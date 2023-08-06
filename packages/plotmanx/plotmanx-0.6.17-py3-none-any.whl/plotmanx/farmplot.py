import contextlib
import glob
import os
import re
from subprocess import Popen, PIPE, STDOUT

import psutil

from . import configuration
from .configuration import PlotmanConfig
from .util import plot_util


def is_plot_moving(cmdline: list) -> bool:
    return (
            len(cmdline) > 3
            and cmdline[0].endswith('plmo')
    )


def is_plmo_nfs(cmdline: list) -> bool:
    test = " ".join(cmdline)
    m = re.match(r"^\/mnt\/nfs.*.?(\d+).\/", test)
    if m:
        return True
    else:
        return False


class FarmPlot:
    """
    The final state to move files from tmp folder to given network hard drive devices
    """

    def __init__(self, cfg: PlotmanConfig):
        self.dsts = cfg.directories.dst
        self.checktmps = cfg.directories.tmp
        self.schedule = cfg.scheduling.polling_time_s
        self.log_file_path = configuration.get_log_path()

    @staticmethod
    def get_running_moving_jobs() -> list:
        jobs = []

        for proc in psutil.process_iter(['pid', 'cmdline']):
            # Ignore processes which most likely have terminated between the time of iteration and data access.
            with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied):
                if is_plot_moving(proc.cmdline()):
                    job = " ".join(proc.cmdline())
                    jobs.append(job)

        return jobs

    @staticmethod
    def get_nfs_details() -> list:
        nfs_list = []

        for proc in psutil.process_iter(['pid', 'cmdline']):
            # Ignore processes which most likely have terminated between the time of iteration and data access.
            with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied):
                if is_plot_moving(proc.cmdline()):
                    if is_plmo_nfs(proc.cmdline()):
                        test = " ".join(proc.cmdline())
                        g = re.match('(\d+)', test)
                        nfs_list.append(g[0])

        return nfs_list

    def start_nfs(self) -> None:

        count1 = len(glob.glob1("~/chia-blockchain", "plmo"))
        if count1 >= 1:
            for d in self.dsts:
                p = Popen(["./plmo", self.checktmps, d, 50000000, self.log_file_path], stdout=PIPE, stderr=STDOUT)
                output, error = p.communicate()
                output = output.strip().decode("utf-8")
                print("start moving file from temp folder to network FS farm location {}".format(d))
                if p.returncode:
                    print(f"E: {output}")
        else:
            print("Did not find the plmo executable.")

    def start_nvme_local_dir(self) -> None:
        subs = [x[0] for x in os.walk("/mnt")]
        count2 = len(subs)
        for rsub in subs:
            print(rsub)

    def maintainence(self, jobs: list) -> None:
        plot_util.tidy_up(jobs, self.checktmps)
