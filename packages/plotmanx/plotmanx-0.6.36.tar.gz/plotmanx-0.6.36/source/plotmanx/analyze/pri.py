import os
import re
import time
from datetime import datetime

from ..util.plot_util import parse_chia_plot_time, get_plot_progress


def errorLineStatus(line: str) -> (bool, bool):
    disk_space = False
    read_failure = False
    m = re.match(r'^Only wrote (\d+) of (\d+) bytes at offset (\d+) from (.+)', line)
    if m:
        disk_space = True

    m = re.match(r'^Only read (\d+) of (\d+) bytes at offset (\d+) from (.+)', line)
    if m:
        read_failure = True

    return disk_space, read_failure


def errorLine(line: str) -> bool:
    disk_space, read_failure = errorLineStatus(line)
    return disk_space or read_failure


class LogFile:
    """
    basic checking and analyzer for this log file
    """

    def __init__(self, logfilename: str):
        self.path = logfilename
        self._total_plots = 0
        self._total_T = 0
        self._pid = 0
        self._produced = 0
        self._start_time = 0
        self._current_plot_id = '--------'
        self._phase = (0, 0)
        self._phase_time = dict()
        self._progress = 0
        self._err_lines = 0
        self._io_failure = False
        self._disk_tight = False

    @property
    def getPhase(self):
        return self._phase

    @property
    def getStartTime(self):
        return self._start_time

    @property
    def getPid(self) -> int:
        return self._pid

    @property
    def getPlotIdFull(self) -> str:
        return self._current_plot_id

    @property
    def getPlotIdShort(self) -> str:
        return self._current_plot_id[:8]

    @property
    def getProductionTPlotSize(self) -> float:
        return self._total_T

    @property
    def getProgressPercentage(self) -> float:
        return self._progress

    @property
    def completedJobs(self):
        return self._produced

    def count_lines(self, adjust: int = 0) -> int:
        with open(self.path, 'r') as v:
            filedat = v.read()
            lin_count = int(filedat.count('\n') + 1)
        c = lin_count - adjust
        return c

    def read_last_line(self) -> str:
        last_line = ''
        with open(self.path, 'r') as f:
            last_line = f.readlines()[-1]
        return last_line

    # Initialize data that needs to be loaded from the logfile
    def init_logfile(self):
        """
        Read plot ID and job start time from logfile.  Return true if we
           find all the info as expected, false otherwise
        """

        assert self.path
        # Try reading for a while; it can take a while for the job to get started as it scans
        # existing plot dirs (especially if they are NFS).

        found_id = False
        found_log = False
        plots = 0
        line_z = 0
        line_zz = 0
        line_err = 0

        for attempt_number in range(3):
            plots = 0
            line_z = 0
            with open(self.path, 'r') as f:

                for line in f:
                    line_z += 1
                    m = re.match('^ID: ([0-9a-f]*)', line)
                    if m:
                        self._current_plot_id = m.group(1)
                        found_id = True

                    m = re.match(r'^Starting phase 1/4:.*\.\.\. (.*)', line)
                    if m:
                        # Mon Nov  2 08:39:53 2020
                        self._start_time = parse_chia_plot_time(m.group(1))
                        found_log = True
                        # continue and looking for the last

                    m = re.match(r'^Renamed final file from', line)

                    if m:
                        plots += 1
                        line_zz = line_z
                        line_err = 0

                    if errorLine(line):
                        line_err += 1

            if found_id and found_log:
                break  # Stop trying
            else:
                print("try to look for the log file again.")
                time.sleep(1)  # Sleep and try again

        if not found_log:
            self._start_time = datetime.fromtimestamp(os.path.getctime(self.path))
        self._produced = plots
        self._err_lines = line_err
        total_lines = self.count_lines()

        print(f"error lines from the last plotting {self._err_lines}, full lines {total_lines}")

        self._progress = get_plot_progress(self.count_lines(line_err + line_zz))

        # Load things from logfile that are dynamic
        self.updatePhases()
        # self.updateGeneratePlots()

    def updatePhases(self):
        assert self.path

        # Map from phase number to subphase number reached in that phase.
        # Phase 1 subphases are <started>, table1, table2, ...
        # Phase 2 subphases are <started>, table7, table6, ...
        # Phase 3 subphases are <started>, tables1&2, tables2&3, ...
        # Phase 4 subphases are <started>
        phase_subphases = {}
        plots = 0
        phase = 0
        plotpool = 0
        line_z = 0
        line_zz = 0
        line_err = 0

        disk_space = False
        read_failure = False

        with open(self.path, 'r') as f:
            for line in f:
                line_z = line_z + 1
                m = re.match('^ID: ([0-9a-f]*)', line)
                if m:
                    self._current_plot_id = m.group(1)

                # "Starting phase 1/4: Forward Propagation into tmp files... Sat Oct 31 11:27:04 2020"
                m = re.match(r'^Starting phase (\d).*', line)
                if m:
                    phase = int(m.group(1))
                    phase_subphases[phase] = 0

                # Phase 1: "Computing table 2"
                m = re.match(r'^Computing table (\d).*', line)
                if m:
                    phase_subphases[1] = max(phase_subphases[1], int(m.group(1)))

                # Phase 2: "Backpropagating on table 2"
                m = re.match(r'^Backpropagating on table (\d).*', line)
                if m:
                    phase_subphases[2] = max(phase_subphases[2], 7 - int(m.group(1)))

                # Phase 3: "Compressing tables 4 and 5"
                m = re.match(r'^Compressing tables (\d) and (\d).*', line)
                if m:
                    phase_subphases[3] = max(phase_subphases[3], int(m.group(1)))

                # "Time for phase 1 = 22796.7 seconds. CPU (98%) Tue Sep 29 17:57:19 2020"
                for phase_t in ['1', '2', '3', '4']:
                    m = re.match(r'^Time for phase ' + phase_t + ' = (\d+.\d+) seconds..*', line)
                    if m:
                        self._phase_time.setdefault(f"ph{phase_t}", float(m.group(1)))

                # Total time = 49487.1 seconds. CPU (97.26%) Wed Sep 30 01:22:10 2020
                # m = re.match(r'^Total time = (\d+.\d+) seconds.*', line)
                # if m:
                # data.setdefault(key, {}).setdefault('total time', []).append(float(m.group(1)))
                m = re.match(r'^Final File size: (\d+.\d+).*', line)
                if m:
                    size = float(m.group(1))
                    plotpool = plotpool + size

                m = re.match(r'^Renamed final file from', line)
                if m:
                    phase = 0
                    phase_subphases = {}
                    plots += 1
                    line_zz = line_z
                    line_err = 0

                if errorLine(line):
                    line_err += 1

        a, b = errorLineStatus(self.read_last_line())
        if a:
            self._disk_tight = True
        if b:
            self._io_failure = True

        self._progress = get_plot_progress(self.count_lines(line_err + line_zz))

        if phase_subphases:
            phase = max(phase_subphases.keys())
            self._phase = (phase, phase_subphases[phase])
        else:
            self._phase = (0, 0)

        self._produced = plots

        if plotpool > 0:
            self._total_T = plotpool / 1000

    @property
    def disk_confirm(self):
        return self._disk_tight

    @property
    def failure_read(self):
        return self._io_failure

    def print(self):
        print(f"total T size: {self._total_T}")
        print(f"current plot id: {self._current_plot_id}")
        print(f"pid: {self._pid}")
        print(f"produced plots: {self._produced}")
