import contextlib
import math
import os
import re

import pendulum
import pkg_resources
import psutil
from psutil.tests import sh

GB = 1_000_000_000

# IN GB size
KSIZE = {
    "32": 256.6,
    "33": 550,
    "34": 1118,
    "35": 2335,
}

# IN GB size
PLOT_SIZE = {
    "32": 108.837,
    "33": 224.227,
    "34": 461.535,
    "35": 949.3,
}

PLOT_LIST = {
    "32": r'^plot-k32-.*plot$',
    "33": r'^plot-k33-.*plot$',
    "34": r'^plot-k34-.*plot$',
    "35": r'^plot-k35-.*plot$',
}

PROGRESS_BAR = {
    "phase1_line_end": 801,
    "phase2_line_end": 834,
    "phase3_line_end": 2474,
    "phase4_line_end": 2620,
    "phase1_weight": 33.4,
    "phase2_weight": 20.43,
    "phase3_weight": 42.29,
    "phase4_weight": 3.88,
}


def is_phase_start(phase_pair) -> bool:
    (ph, subph) = phase_pair
    return ph < 3 and subph < 6


def phase_str(phase_pair) -> str:
    (ph, subph) = phase_pair
    return ((str(ph) if ph is not None else '?') + ':'
            + (str(subph) if subph is not None else '?'))


def abbr_path(path, putative_prefix) -> str:
    if putative_prefix and path.startswith(putative_prefix):
        return os.path.relpath(path, putative_prefix)
    else:
        return path


def df_b(d) -> int:
    """
    Return free space for directory (in bytes)
    """
    stat = os.statvfs(d)
    return stat.f_frsize * stat.f_bavail


def checkTempSpace(k_number: int, tmpdir: str) -> bool:
    for k, v in KSIZE.items():
        if int(k) == k_number:
            gb_free = df_b(tmpdir) / GB
            if gb_free > float(v):
                return True
    return False


def isSpaceCritical(tmpdir: str) -> bool:
    """
    determine when the current working directory is on critical free space limitzxzx
    """

    gb_free = df_b(tmpdir) / GB
    if gb_free < 1:
        return True
    else:
        return False


def availableSpace(tmpdir: str) -> str:
    gb_free = df_b(tmpdir) / GB
    return f"{gb_free} GB"


def get_k32_plotsize() -> float:
    v = PLOT_SIZE["32"]
    return v * GB


def human_format(num, precision):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return (('%.' + str(precision) + 'f%s') %
            (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude]))


def time_format(sec):
    if sec is None:
        return '-'
    if sec < 60:
        return '%ds' % sec
    else:
        return '%d:%02d' % (int(sec / 3600), int((sec % 3600) / 60))


def tmpdir_phases_str(tmpdir_phases_pair):
    tmpdir = tmpdir_phases_pair[0]
    phases = tmpdir_phases_pair[1]
    phase_str = ', '.join(['%d:%d' % ph_subph for ph_subph in sorted(phases)])
    return ('%s (%s)' % (tmpdir, phase_str))


def getMaxFitablePlots(drive_size: int, final_plot_size: int) -> float:
    driveSpaceBuffer = 0.05
    amt = ((drive_size - (drive_size * driveSpaceBuffer))) / final_plot_size
    return amt


def availableSizeDriveForPlots(sized: int, final_plot_size: int) -> float:
    return sized / final_plot_size


def split_path_prefix(items):
    if not items:
        return ('', [])

    prefix = os.path.commonpath(items)
    if prefix == '/':
        return ('', items)
    else:
        remainders = [os.path.relpath(i, prefix) for i in items]
        return (prefix, remainders)


def list_k32_plots(d) -> list:
    """List completed k32 plots in a directory (not recursive)"""
    return list_k_plots(d, 32)


def list_k_plots(d: str, K: int) -> list:
    plots = []
    for plot in os.listdir(d):
        if re.match(PLOT_LIST[str(K)], plot):
            plot = os.path.join(d, plot)
            try:
                require_size = PLOT_SIZE[str(K)] * 0.95 * GB
                if os.stat(plot).st_size > require_size:
                    plots.append(plot)
            except FileNotFoundError:
                continue

    return plots


def column_wrap(items, n_cols, filler=None) -> list:
    '''Take items, distribute among n_cols columns, and return a set
       of rows containing the slices of those columns.'''
    rows = []
    n_rows = math.ceil(len(items) / n_cols)
    for row in range(n_rows):
        row_items = items[row:: n_rows]
        # Pad and truncate
        rows.append((row_items + ([filler] * n_cols))[:n_cols])
    return rows


def get_frw_status(job) -> str:
    f = "Y" if job.isFrozen else "N"
    r = "Y" if job.isReadFail else "N"
    w = "Y" if job.isWroteErr else "N"
    return f"{f}/{r}/{w}"


def parse_chia_plot_time(s):
    # This will grow to try ISO8601 as well for when Chia logs that way
    return pendulum.from_format(s, 'ddd MMM DD HH:mm:ss YYYY', locale='en', tz=None)


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]


def chia_version() -> str:
    plot_args = ['chia', 'version']
    try:
        version = os.popen(" ".join(plot_args), 'r').read().rstrip("\n")
    except TypeError:
        version = 'undetected'
    except ValueError:
        version = 'undetected'

    return version


def plotman_version() -> str:
    return pkg_resources.get_distribution('plotmanx').version


def get_plot_progress(line_count: int) -> float:
    phase1_line_end = PROGRESS_BAR.get('phase1_line_end')
    phase2_line_end = PROGRESS_BAR.get('phase2_line_end')
    phase3_line_end = PROGRESS_BAR.get('phase3_line_end')
    phase4_line_end = PROGRESS_BAR.get('phase4_line_end')
    phase1_weight = PROGRESS_BAR.get('phase1_weight')
    phase2_weight = PROGRESS_BAR.get('phase2_weight')
    phase3_weight = PROGRESS_BAR.get('phase3_weight')
    phase4_weight = PROGRESS_BAR.get('phase4_weight')
    progress = 0
    if line_count > phase1_line_end:
        progress += phase1_weight
    else:
        progress += phase1_weight * (line_count / phase1_line_end)
        return progress
    if line_count > phase2_line_end:
        progress += phase2_weight
    else:
        progress += phase2_weight * ((line_count - phase1_line_end) / (phase2_line_end - phase1_line_end))
        return progress
    if line_count > phase3_line_end:
        progress += phase3_weight
    else:
        progress += phase3_weight * ((line_count - phase2_line_end) / (phase3_line_end - phase2_line_end))
        return progress
    if line_count > phase4_line_end:
        progress += phase4_weight
    else:
        progress += phase4_weight * ((line_count - phase3_line_end) / (phase4_line_end - phase3_line_end))


    return progress


def tidy_up(jobs: list, temp_folders: list) -> None:
    active_plot_ids = [r.plot_id for r in jobs]
    count_files = 0
    remove_paths = []

    for d in temp_folders:
        print(f"🚧 check {d}")
        with os.scandir(d) as it:
            for entry in it:
                if not entry.name.endswith('.plot') and entry.is_file() and not entry.name.endswith(".db"):
                    print(f"📥 check file {entry.name}")
                    if len(active_plot_ids) > 0:
                        found = False
                        for actId in active_plot_ids:
                            if actId in entry.name:
                                found = True
                                break

                        if not found:
                            print(f"✅ qualified file {entry.name}")
                            remove_paths.append(entry.path)
                    else:
                        print(f"✅ qualified file {entry.name}")
                        remove_paths.append(entry.path)

    print("-------------------------")
    print("Active plot ids:")
    print(active_plot_ids)

    for u in remove_paths:
        try:
            os.unlink(u)
            count_files = count_files + 1
            print(f"Found and removed unrelated tmp {u}...")
        except FileNotFoundError:
            print(f"Failed to remove file {u}")
            pass

    print("-------------------------")
    print(f"complete total {count_files} files removed")


def discover_local_hhd() -> list:
    # test psutil.disk_usage() and psutil.disk_partitions()
    # against "df -a"
    def dff(path):
        output = sh('df -P -B 1 "%s"' % path).strip()
        # df = Popen(["df", "-P", "-B", "1", path], stdout=PIPE)
        # output = df.communicate()[0]

        lines = output.split('\n')
        lines.pop(0)
        line = lines.pop(0)
        dev, total, used, free = line.split()[:4]
        if dev == 'none':
            dev = ''
        total, used, free = int(total), int(used), int(free)
        return dev, total, used, free

    devices = []
    for part in psutil.disk_partitions(all=False):
        dev, total, used, free = dff(part.mountpoint)

        g = re.match("^\/dev\/sd([a-z])$", dev)

        if g:
            usage = psutil.disk_usage(part.mountpoint)
            print(f"found - {dev} {part.mountpoint} {usage}")
            percent = float(used / total * 100)

            # assert usage.total == total
            # 10 MB tollerance

            if abs(usage.free - free) > 10 * 1024 * 1024:
                print("psutil=%s, df=%s" % (usage.free, free))
            if abs(usage.used - used) > 10 * 1024 * 1024:
                print("psutil=%s, df=%s" % (usage.used, used))

            lowCap = False
            if usage.free < 100 * GB:
                lowCap = True

            devices.append(dict(disk=dev, per=percent, low=lowCap))

    return devices


def discover_nvme_io() -> list:
    devices = []
    try:
        disk_counters = psutil.disk_io_counters(perdisk=True)
        # print(disk_counters)
        for device_name in disk_counters:
            m0 = re.match("^nvme(.*)$", device_name)
            if m0:
                counters = disk_counters[device_name]
                gbpersec = float(counters.write_bytes) / GB
                print(f'Disk I/O counters device - {device_name}: {gbpersec} gb/s')
                devices.append(dict(dev=device_name, speed=gbpersec))

    except OSError as e:
        print(u'Caught exception when crawling disk I/O counters: {0}'.format(e))
    except TypeError as v:
        print("there is an type error.")

    return devices


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


def discover_plmo_operations():
    jobs = []

    for proc in psutil.process_iter(['pid', 'cmdline']):
        # Ignore processes which most likely have terminated between the time of iteration and data access.
        with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied):
            if is_plot_moving(proc.cmdline()):
                job = " ".join(proc.cmdline())
                jobs.append(job)

    return jobs


def discover_nfs_operations() -> list:
    nfs_list = []
    try:
        for proc in psutil.process_iter(['pid', 'cmdline']):
            # Ignore processes which most likely have terminated between the time of iteration and data access.
            with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied):
                if is_plot_moving(proc.cmdline()):
                    if is_plmo_nfs(proc.cmdline()):
                        test = " ".join(proc.cmdline())
                        print(f"check path: {test}")
                        g = re.match('(\d+)', test)
                        nfs_list.append(f"192.168.10.{g[0]}")

    except TypeError as b:
        print(f"Type Error: {b}")
    return nfs_list
