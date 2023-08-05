import contextlib
import glob
import re
from subprocess import Popen, PIPE, STDOUT

import psutil

from . import configuration
from .configuration import PlotmanConfig


def is_plot_moving(cmdline) -> bool:
    return (
            len(cmdline) > 3
            and cmdline[0].endswith('plmo')
    )


def is_plmo_nfs(cmdline: str) -> bool:
    m = re.match('^\/mnt\/nfs.*.?(\d+).\/', cmdline)
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
                        g = re.match('(\d+)', proc.cmdline())
                        nfs_list.append(g[0])

        return nfs_list

    def start_copyplot_spawn(self):

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
