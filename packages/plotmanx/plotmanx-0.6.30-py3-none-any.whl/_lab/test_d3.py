import re

import psutil
from psutil.tests import sh


def check_mount_sd(mountpoint: str) -> bool:
    g = re.match("^\/dev\/sd([a-z])$", mountpoint)
    if g:
        return True
    else:
        return False


def test_disk_partitions_and_usage():
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

    for part in psutil.disk_partitions(all=False):

        dev, total, used, free = dff(part.mountpoint)
        if check_mount_sd(dev):
            usage = psutil.disk_usage(part.mountpoint)
            print(f"found - part {part.mountpoint}")
            print(dev)
            print(usage)

            # assert usage.total == total
            # 10 MB tollerance
            if abs(usage.free - free) > 10 * 1024 * 1024:
                print("psutil=%s, df=%s" % (usage.free, free))
            if abs(usage.used - used) > 10 * 1024 * 1024:
                print("psutil=%s, df=%s" % (usage.used, used))


print("before __name__ guard")
if __name__ == '__main__':
    # disks = [d.mountpoint for d in psutil.disk_partitions()]
    # disks_usage = [psutil.disk_usage(d) for d in disks]
    # print(disks_usage)

    test_disk_partitions_and_usage()

print("after __name__ guard")
