import concurrent.futures
import datetime
import glob
import operator
import os
import subprocess

import pendulum
import pkg_resources
import psutil

from .configuration import Scheduling, Directories, Plotting
from .farmplot import FarmPlot
from .job import Job, job_phases_for_tmpdir
from .manager import phases_permit_new_job
from .util import plot_util
# Plotman libraries
from .util.plot_util import getIP, isSpaceCritical

MIN = 60  # Seconds
HR = 3600  # Seconds
MAX_PLOT_SIZE = 332  # Minimum gb required for k32 plot
MAX_AGE = 1000_000_000  # Arbitrary large number of seconds


def terminate(job: Job) -> None:
    job.suspend()
    temp_files = job.get_temp_files()
    job.cancel()
    for f in temp_files:
        os.remove(f)


class MintJ:
    def __init__(self, plotting_cfg: Plotting):
        self.parallel = 0
        self.cpu_clock = 0
        self.youngest_job_age = 0
        self.global_stagger = 0
        self.global_max_jobs = 0
        self.global_stagger_m = 0
        self.wait_reason = None
        self.aging_reason = None
        self.jobs = None
        self.plotdaemon = False
        self.readIoIssue = 0
        self.schedule_x = None
        self.dir_cfg_x = None
        self.plotcfg_x = plotting_cfg
        self.bulkn = 0

        self.disk_bytes_read_last = 0
        self.disk_bytes_write_last = 0
        self.net_bytes_read_last = 0
        self.net_bytes_write_last = 0
        self.iowait_last = 0

    def Upcfg(self, schedule: Scheduling, plotting_cfg: Plotting):
        self.schedule_x = schedule
        self.plotcfg_x = plotting_cfg
        self.global_max_jobs = schedule.global_max_jobs
        self.global_stagger_m = schedule.global_stagger_m
        self.youngest_job_age = min(self.jobs, key=Job.get_time_wall).get_time_wall() if self.jobs else MAX_AGE
        self.global_stagger = int(self.global_stagger_m[self.cpu_clock] * MIN)
        self.parallel = schedule.parallel

    def GenJobs(self, dir_cfg: Directories):
        self.dir_cfg_x = dir_cfg
        self.jobs = Job.genTasks(dir_cfg.log)

    def CacheGenJobs(self, dir_cfg: Directories):
        self.jobs = Job.genTasks(dir_cfg.log, cached_jobs=self.jobs)

    @property
    def WaitLog(self) -> str:
        return self.wait_reason

    @property
    def LsJobs(self) -> list:
        return self.jobs

    @property
    def isClockReady(self) -> bool:
        return self.youngest_job_age < self.global_stagger

    @property
    def isCreateNewJobParallelReady(self) -> bool:
        return self.youngest_job_age > self.global_stagger or len(self.jobs) == 0

    @property
    def NewLogFile(self) -> str:
        return os.path.join(self.dir_cfg_x.log, pendulum.now().isoformat(timespec='microseconds').replace(':', '_') + '.log')

    def JobCreate(self):
        if psutil.cpu_percent(interval=10) > 99:
            self.wait_reason = 'cpu optimized!'

        elif self.isClockReady and self.parallel <= 1:
            self.wait_reason = 'stagger (%ds/%ds)' % (self.youngest_job_age, self.global_stagger)

        elif len(self.jobs) >= self.global_max_jobs:
            self.wait_reason = 'max jobs (%d)' % self.global_max_jobs

        else:

            tmp_to_all_phases = [(d, job_phases_for_tmpdir(d, self.jobs)) for d in self.dir_cfg_x.tmp]

            eligible = [(d, phases) for (d, phases) in tmp_to_all_phases
                        if phases_permit_new_job(phases, d, self.schedule_x, self.dir_cfg_x)]

            rankable = [(d, phases[0]) if phases else (d, (999, 999)) for (d, phases) in eligible]

            if not eligible:
                self.wait_reason = 'no eligible tempdirs'
            else:
                # Plot to oldest tmpdir.
                tmpdir = max(rankable, key=operator.itemgetter(1))[0]
                # Select the dst dir least recently selected

                if plot_util.checkTempSpace(int(self.plotcfg_x.k), tmpdir):

                    logfile = self.NewLogFile

                    plot_args = ['chia', 'plots', 'create',
                                 '-k', str(self.plotcfg_x.k),
                                 '-r', str(self.plotcfg_x.n_threads),
                                 '-u', str(self.plotcfg_x.n_buckets),
                                 '-b', str(self.plotcfg_x.job_buffer),
                                 '-n 32',
                                 '-t', tmpdir,
                                 '-d', tmpdir]

                    if self.plotcfg_x.e:
                        plot_args.append('-e')

                    if self.plotcfg_x.farmer_pk is not None:
                        plot_args.append('-f')
                        plot_args.append(self.plotcfg_x.farmer_pk)

                    if self.plotcfg_x.pool_pk is not None:
                        plot_args.append('-p')
                        plot_args.append(self.plotcfg_x.pool_pk)

                    if self.dir_cfg_x.tmp2 is not None:
                        plot_args.append('-2')
                        plot_args.append(self.dir_cfg_x.tmp2)

                    logmsg = ('Starting plot job: %s ; logging to %s' % (' '.join(plot_args), logfile))

                    self.wait_reason = logmsg

                    try:
                        open_log_file = open(logfile, 'x')
                    except FileExistsError:
                        # The desired log file name already exists.  Most likely another
                        # plotman process already launched a new process in response to
                        # the same scenario that triggered us.  Let's at least not
                        # confuse things further by having two plotting processes
                        # logging to the same file.  If we really should launch another
                        # plotting process, we'll get it at the next check cycle anyways.
                        self.wait_reason = (
                            f'Plot log file already exists, skipping attempt to start a'
                            f' new plot: {logfile!r}'
                        )
                        return False

                    # start_new_sessions to make the job independent of this controlling tty.
                    p = subprocess.Popen(plot_args,
                                         stdout=open_log_file,
                                         stderr=subprocess.STDOUT,
                                         start_new_session=True)

                    psutil.Process(p.pid).nice(0)

                    return True
                else:
                    self.wait_reason = f'disk space is not enough! there is only {plot_util.availableSpace(tmpdir)} available in {tmpdir}.'

        return False

    def PlotDaemon(self):
        self.plotdaemon = True

    def SpaceManagement(self) -> None:
        for d in self.dir_cfg_x.tmp:
            ls = []
            if isSpaceCritical(d):
                for j in self.jobs:
                    if j.isFrozen is True:
                        (size, plotid) = MintJ.terminateJob(j)
                        print(f'remove from frozen job for space, with temp size {size} [{plotid}]')

                    elif j.isWroteErr is True or plot_util.is_phase_start(j.progress()) is True:
                        ls.append(j)

            if len(ls) > 0:
                for i, j in enumerate(sorted(ls, key=Job.get_tmp_usage)):
                    (size, plotid) = MintJ.terminateJob(j)
                    print(f'remove temp files for space from sorted temp size {size} [{plotid}]')
                    break

        self.readIoIssue = 0

        for j in self.jobs:
            if j.isFrozen is True:
                (size, plotid) = MintJ.terminateJob(j)
                print(f'remove from frozen job for good {size} [{plotid}]')

            if j.isReadFail is True:
                print(f'failure from read io: [{j.plot_id}]. possible disk failure or io failure... ')
                self.readIoIssue = self.readIoIssue + 1

    @staticmethod
    def terminateJob(j: Job) -> any:
        size = plot_util.human_format(j.get_tmp_usage(), 0)
        id = j.plot_id
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(terminate, j)
        return (size, id)

    def ParallelWorker(self):
        for i in range(self.parallel):
            sw = self.bulkn % self.parallel
            g = (self.bulkn - sw) / self.parallel

            if g % 2 == 0:
                self.cpu_clock = 0
            else:
                self.cpu_clock = 1

            started = self.JobCreate()
            self.bulkn = self.bulkn + 1
            if not self.plotdaemon:
                if started:
                    self.wait_reason = '<just started job>'
                    self.CacheGenJobs(self.dir_cfg_x)
            else:
                ts = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
                if self.wait_reason:
                    print('> %s, %s' % (ts, self.wait_reason))
                else:
                    print('start plot > %s' % ts)

    def GenStatus(self, jobs: list) -> dict:
        count1 = len(glob.glob1("/mnt/local/tmp", "*.plot"))
        count2 = len(glob.glob1("/mnt/local/temp", "*.plot"))
        count3 = len(glob.glob1("/mnt/nvme/temp", "*.plot"))
        count4 = len(glob.glob1("/mnt/nvme1n0/temp", "*.plot"))

        fcount = count1 + count2 + count3 + count4
        listplmo = FarmPlot.get_running_moving_jobs()
        nfslist = FarmPlot.get_nfs_details()

        disk = psutil.disk_io_counters()
        disk_bytes_read, disk_bytes_write = disk.read_bytes, disk.write_bytes
        net = psutil.net_io_counters()
        net_bytes_read, net_bytes_write = net.bytes_recv, net.bytes_sent
        iowait = psutil.cpu_times().iowait

        disks = [d.mountpoint for d in psutil.disk_partitions()]
        disks_usage = [psutil.disk_usage(d) for d in disks]
        disks_used = sum(d.used for d in disks_usage)
        disks_total = sum(d.total for d in disks_usage)

        d_info = dict(
            jobls=[i.toJson() for i in jobs],
            historyplots=sum([i.exportProductionPlots for i in jobs]),
            sizet=sum([h.exportSize for h in jobs]),
            plotcount=fcount,
            io_read_issues=self.readIoIssue,
            movingcount=len(listplmo),
            movingdetail=listplmo,
            nfsips=nfslist,
            cpucount=psutil.cpu_count(),
            stamp=int(datetime.datetime.now().timestamp()),
            version=pkg_resources.get_distribution('plotmanx').version,

            cpu_percent=psutil.cpu_percent(),
            memory_percent=psutil.virtual_memory().percent,
            cache_percent=round(psutil.virtual_memory().cached / psutil.virtual_memory().total * 100, 1),
            slab_percent=round(psutil.virtual_memory().slab / psutil.virtual_memory().total * 100, 1),
            swap_percent=psutil.swap_memory().percent,
            disk_percent=round((disks_used / disks_total * 100), 2),
            iowait_percent=round((iowait - self.iowait_last) / psutil.cpu_count() * 100, 1),
            net_read_mb_s='{:,}'.format(int((net_bytes_read - self.net_bytes_read_last) / 1024 / 1024)),
            net_write_mb_s='{:,}'.format(int((net_bytes_write - self.net_bytes_write_last) / 1024 / 1024)),
            disk_read_mb_s='{:,}'.format(int((disk_bytes_read - self.disk_bytes_read_last) / 1024 / 1024)),
            disk_write_mb_s='{:,}'.format(int((disk_bytes_write - self.disk_bytes_write_last) / 1024 / 1024)),
            # lsof='{:,}'.format(int(subprocess.check_output('lsof | wc -l', shell=True).decode())),
            net_fds='{:,}'.format(len(psutil.net_connections())),
            identity=getIP(),
        )

        self.net_bytes_read_last, self.net_bytes_write_last = net_bytes_read, net_bytes_write
        self.disk_bytes_read_last, self.disk_bytes_write_last = disk_bytes_read, disk_bytes_write
        self.iowait_last = iowait

        return d_info
