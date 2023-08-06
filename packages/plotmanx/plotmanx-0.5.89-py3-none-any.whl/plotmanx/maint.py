import os

from .configuration import Directories


def archive_old_log_files(jobs: list, dir: Directories):
    running_logs = [os.path.basename(jb.getLogPath) for jb in jobs]
    archive_files = []
    for root, dirs, files in os.walk(dir.log, topdown=True):
        for f in files:
            if f[-4:] in ['.log', '.txt']:
                if f not in running_logs:
                    archive_files.append(f)



