import math
import os
import re
import socket

import pendulum

GB = 1_000_000_000

KSIZE = {
    "32": 256.6,
    "33": 550,
    "34": 1118,
    "35": 2335,
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
    'Return free space for directory (in bytes)'
    stat = os.statvfs(d)
    return stat.f_frsize * stat.f_bavail


def checkTempSpace(knm: int, tmpdir: str) -> bool:
    for k, v in KSIZE.items():
        if int(k) == knm:
            gb_free = df_b(tmpdir) / GB
            if gb_free > float(v):
                return True
    return False


def isSpaceCritical(tmpdir: str) -> bool:
    gb_free = df_b(tmpdir) / GB
    if gb_free < 0.1:
        return True
    else:
        return False


def availableSpace(tmpdir: str) -> str:
    gb_free = df_b(tmpdir) / GB
    return f"{gb_free} GB"


def get_k32_plotsize():
    return 108 * GB


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


def list_k32_plots(d):
    """List completed k32 plots in a directory (not recursive)"""
    plots = []
    for plot in os.listdir(d):
        if re.match(r'^plot-k32-.*plot$', plot):
            plot = os.path.join(d, plot)
            try:
                if os.stat(plot).st_size > (0.95 * get_k32_plotsize()):
                    plots.append(plot)
            except FileNotFoundError:
                continue

    return plots


def column_wrap(items, n_cols, filler=None):
    '''Take items, distribute among n_cols columns, and return a set
       of rows containing the slices of those columns.'''
    rows = []
    n_rows = math.ceil(len(items) / n_cols)
    for row in range(n_rows):
        row_items = items[row:: n_rows]
        # Pad and truncate
        rows.append((row_items + ([filler] * n_cols))[:n_cols])
    return rows


def is_freezed(job):
    return 'YES' if job.last_updated_time_in_min > 60 else 'NO'


def parse_chia_plot_time(s):
    # This will grow to try ISO8601 as well for when Chia logs that way
    return pendulum.from_format(s, 'ddd MMM DD HH:mm:ss YYYY', locale='en', tz=None)


def get_ip_address(ifname: str) -> str:
    """ s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     return socket.inet_ntoa(fcntl.ioctl(
         s.fileno(),
         0x8915,  # SIOCGIFADDR
         struct.pack('256s', ifname[:15])
     )[20:24])
     """
    return socket.gethostname()


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]


def getIP() -> str:
    return get_ip_address('eth0')  # '192.168.0.110'


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
