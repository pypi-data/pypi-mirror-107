import os
import re
import statistics
import time
from datetime import datetime

import texttable as tt

from . import plot_util
from .plot_util import parse_chia_plot_time


class LogFile:
    """
    basic checking and analyzer for this log file
    """

    def __init__(self, logfilename: str):
        self.path = logfilename
        self._total_plots = 0
        self._total_T = 0
        self._pid = 0
        self._start_time = 0
        self._current_plot_id = '--------'
        self._phase = (0, 0)

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
    def getPlotsDoneHistory(self) -> int:
        return self._total_plots

    @property
    def getProductionTPlotSize(self) -> float:
        return self._total_T

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
        for attempt_number in range(3):
            with open(self.path, 'r') as f:
                for line in f:
                    m = re.match('^ID: ([0-9a-f]*)', line)
                    if m:
                        self._current_plot_id = m.group(1)
                        found_id = True
                    m = re.match(r'^Starting phase 1/4:.*\.\.\. (.*)', line)
                    if m:
                        # Mon Nov  2 08:39:53 2020
                        self._start_time = parse_chia_plot_time(m.group(1))
                        found_log = True
                        # continue and looking for the last occurance

            if found_id and found_log:
                break  # Stop trying
            else:
                time.sleep(1)  # Sleep and try again

        # If we couldn't find the line in the logfile, the job is probably just getting started
        # (and being slow about it).  In this case, use the last metadata change as the start time.
        # TODO: we never come back to this; e.g. plot_id may remain uninitialized.
        # TODO: should we just use the process start time instead?

        if not found_log:
            self._start_time = datetime.fromtimestamp(os.path.getctime(self.path))

        # Load things from logfile that are dynamic
        self.set_phase_from_logfile()

    def set_phase_from_logfile(self):
        assert self.path

        # Map from phase number to subphase number reached in that phase.
        # Phase 1 subphases are <started>, table1, table2, ...
        # Phase 2 subphases are <started>, table7, table6, ...
        # Phase 3 subphases are <started>, tables1&2, tables2&3, ...
        # Phase 4 subphases are <started>
        phase_subphases = {}

        with open(self.path, 'r') as f:
            for line in f:
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

                # TODO also collect timing info:

                # "Time for phase 1 = 22796.7 seconds. CPU (98%) Tue Sep 29 17:57:19 2020"
                # for phase in ['1', '2', '3', '4']:
                # m = re.match(r'^Time for phase ' + phase + ' = (\d+.\d+) seconds..*', line)
                # data.setdefault....

                # Total time = 49487.1 seconds. CPU (97.26%) Wed Sep 30 01:22:10 2020
                # m = re.match(r'^Total time = (\d+.\d+) seconds.*', line)
                # if m:
                # data.setdefault(key, {}).setdefault('total time', []).append(float(m.group(1)))

        if phase_subphases:
            phase = max(phase_subphases.keys())
            self._phase = (phase, phase_subphases[phase])
        else:
            self._phase = (0, 0)

    def updateGeneratePlots(self):
        assert self.path
        size_list = []
        grandsize = 0
        plots = 0

        with open(self.path, 'r') as f:
            for line in f:
                m = re.match(r'^Final File size: (\d+.\d+).*', line)
                if m:
                    size = float(m.group(1))
                    size_list.append(size)
                    grandsize = grandsize + size
                    plots += 1

        if grandsize > 0:
            self._total_T = grandsize / 1024
            self._total_plots = plots

    def print(self):
        print(f"total T size: {self._total_T}")
        print(f"total plots: {self._total_plots}")
        print(f"current plot id: {self._current_plot_id}")
        print(f"pid: {self._pid}")


def analyze(logfilenames, clipterminals, bytmp, bybitfield):
    data = {}
    for logfilename in logfilenames:
        with open(logfilename, 'r') as f:
            # Record of slicing and data associated with the slice
            sl = 'x'  # Slice key
            phase_time = {}  # Map from phase index to time
            n_sorts = 0
            n_uniform = 0
            is_first_last = False

            # Read the logfile, triggering various behaviors on various
            # regex matches.
            for line in f:
                # Beginning of plot job.  We may encounter this multiple
                # times, if a job was run with -n > 1.  Sample log line:
                # 2021-04-08T13:33:43.542  chia.plotting.create_plots       : INFO     Starting plot 1/5
                m = re.search(r'Starting plot (\d*)/(\d*)', line)
                if m:
                    # (re)-initialize data structures
                    sl = 'x'  # Slice key
                    phase_time = {}  # Map from phase index to time
                    n_sorts = 0
                    n_uniform = 0

                    seq_num = int(m.group(1))
                    seq_total = int(m.group(2))
                    is_first_last = seq_num == 1 or seq_num == seq_total

                # Temp dirs.  Sample log line:
                # Starting plotting progress into temporary dirs: /mnt/tmp/01 and /mnt/tmp/a
                m = re.search(r'^Starting plotting.*dirs: (.*) and (.*)', line)
                if m:
                    # Record tmpdir, if slicing by it
                    if bytmp:
                        tmpdir = m.group(1)
                        sl += '-' + tmpdir

                # Bitfield marker.  Sample log line(s):
                # Starting phase 2/4: Backpropagation without bitfield into tmp files... Mon Mar  1 03:56:11 2021
                #   or
                # Starting phase 2/4: Backpropagation into tmp files... Fri Apr  2 03:17:32 2021
                m = re.search(r'^Starting phase 2/4: Backpropagation', line)
                if bybitfield and m:
                    if 'without bitfield' in line:
                        sl += '-nobitfield'
                    else:
                        sl += '-bitfield'

                # Phase timing.  Sample log line:
                # Time for phase 1 = 22796.7 seconds. CPU (98%) Tue Sep 29 17:57:19 2020
                for phase in ['1', '2', '3', '4']:
                    m = re.search(r'^Time for phase ' + phase + ' = (\d+.\d+) seconds..*', line)
                    if m:
                        phase_time[phase] = float(m.group(1))

                # Uniform sort.  Sample log line:
                # Bucket 267 uniform sort. Ram: 0.920GiB, u_sort min: 0.688GiB, qs min: 0.172GiB.
                #   or
                # ....?....
                #   or
                # Bucket 511 QS. Ram: 0.920GiB, u_sort min: 0.375GiB, qs min: 0.094GiB. force_qs: 1
                m = re.search(r'Bucket \d+ ([^\.]+)\..*', line)
                if m and not 'force_qs' in line:
                    sorter = m.group(1)
                    n_sorts += 1
                    if sorter == 'uniform sort':
                        n_uniform += 1
                    elif sorter == 'QS':
                        pass
                    else:
                        print('Warning: unrecognized sort ' + sorter)

                # Job completion.  Record total time in sliced data store.
                # Sample log line:
                # Total time = 49487.1 seconds. CPU (97.26%) Wed Sep 30 01:22:10 2020
                m = re.search(r'^Total time = (\d+.\d+) seconds.*', line)
                if m:
                    if clipterminals and is_first_last:
                        pass  # Drop this data; omit from statistics.
                    else:
                        data.setdefault(sl, {}).setdefault('total time', []).append(float(m.group(1)))
                        for phase in ['1', '2', '3', '4']:
                            data.setdefault(sl, {}).setdefault('phase ' + phase, []).append(phase_time[phase])
                        data.setdefault(sl, {}).setdefault('%usort', []).append(100 * n_uniform // n_sorts)

    # Prepare report
    tab = tt.Texttable()
    all_measures = ['%usort', 'phase 1', 'phase 2', 'phase 3', 'phase 4', 'total time']
    headings = ['Slice', 'n'] + all_measures
    tab.header(headings)
    for sl in data.keys():
        row = [sl]
        # Sample size
        sample_sizes = []
        for measure in all_measures:
            values = data.get(sl, {}).get(measure, [])
            sample_sizes.append(len(values))
        sample_size_lower_bound = min(sample_sizes)
        sample_size_upper_bound = max(sample_sizes)
        if sample_size_lower_bound == sample_size_upper_bound:
            row.append('%d' % sample_size_lower_bound)
        else:
            row.append('%d-%d' % (sample_size_lower_bound, sample_size_upper_bound))

        # Phase timings
        for measure in all_measures:
            values = data.get(sl, {}).get(measure, [])
            if len(values) > 1:
                row.append('μ=%s σ=%s' % (
                    plot_util.human_format(statistics.mean(values), 1),
                    plot_util.human_format(statistics.stdev(values), 0)
                ))
            elif len(values) == 1:
                row.append(plot_util.human_format(values[0], 1))
            else:
                row.append('N/A')

        tab.add_row(row)
    (rows, columns) = os.popen('stty size', 'r').read().split()
    tab.set_max_width(int(columns))
    s = tab.draw()
    print(s)
