import os

# Constants

# Plotman libraries

MIN = 60  # Seconds
HR = 3600  # Seconds
MAX_PLOT_SIZE = 332  # Minimum gb required for k32 plot
MAX_AGE = 1000_000_000  # Arbitrary large number of seconds


def dstdirs_to_furthest_phase(all_jobs):
    '''Return a map from dst dir to a phase tuple for the most progressed job
       that is emitting to that dst dir.'''
    result = {}
    for j in all_jobs:
        if not j.dstdir in result.keys() or result[j.dstdir] < j.progress():
            result[j.dstdir] = j.progress()
    return result


def dstdirs_to_youngest_phase(all_jobs):
    '''Return a map from dst dir to a phase tuple for the least progressed job
       that is emitting to that dst dir.'''
    result = {}
    for j in all_jobs:
        if not j.dstdir in result.keys() or result[j.dstdir] > j.progress():
            result[j.dstdir] = j.progress()
    return result


def phases_permit_new_job(phases, d, sched_cfg, dir_cfg):
    '''Scheduling logic: return True if it's OK to start a new job on a tmp dir
       with existing jobs in the provided phases.'''

    # 当前磁盘剩余空间小于350g不新增
    # if psutil.disk_usage(d).free / 1024 / 1024 / 1024 < 350:
    #    return False

    # Filter unknown-phase jobs
    phases = [ph for ph in phases if ph[0] is not None and ph[1] is not None]

    if len(phases) == 0:
        return True

    milestone = (sched_cfg.tmpdir_stagger_phase_major, sched_cfg.tmpdir_stagger_phase_minor)
    # tmpdir_stagger_phase_limit default is 1, as declared in configuration.py

    if len([p for p in phases if p < milestone]) >= sched_cfg.tmpdir_stagger_phase_limit:
        return False

    # Limit the total number of jobs per tmp dir. Default to the overall max
    # jobs configuration, but restrict to any configured overrides.
    max_plots = sched_cfg.tmpdir_max_jobs
    if dir_cfg.tmp_overrides is not None and d in dir_cfg.tmp_overrides:
        curr_overrides = dir_cfg.tmp_overrides[d]
        if curr_overrides.tmpdir_max_jobs is not None:
            max_plots = curr_overrides.tmpdir_max_jobs
    if len(phases) >= max_plots:
        return False

    return True


def get_size(dir) -> float:
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += (os.path.getsize(fp)) / 1000000000

    return total_size


def anyTmpDirIsNearlyFull(dir_cfg) -> any:
    for dir in dir_cfg.tmp:
        total_size = get_size(dir)
        if total_size > MAX_PLOT_SIZE:
            return (True, total_size, dir)
    return (False, 0, "")


def select_jobs_by_partial_id(jobs, partial_id) -> list:
    selected = []
    for j in jobs:
        if j.isJobStartWithId(partial_id):
            selected.append(j)
    return selected
