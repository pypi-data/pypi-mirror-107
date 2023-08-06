import glob
import os
import re
from subprocess import Popen, PIPE, STDOUT

from . import configuration
from .configuration import PlotmanConfig
from .util import plot_util



class FarmPlot:
    """
    The final state to move files from tmp folder to given network hard drive devices
    """

    def __init__(self, cfg: PlotmanConfig):
        self.dsts = cfg.directories.dst
        self.checktmps = cfg.directories.tmp
        self.schedule = cfg.scheduling.polling_time_s
        self.log_file_path = configuration.get_log_path()

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
