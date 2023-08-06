import re

import psutil
from psutil.tests import sh


def commaInt(x: str) -> int:
    return int(x.replace(',', ''))


# sudo nvme smart-log /dev/nvme0
def dffnvme(path):
    output = sh('sudo nvme smart-log /dev/%s' % path).strip()
    # df = Popen(["df", "-P", "-B", "1", path], stdout=PIPE)
    # output = df.communicate()[0]
    lines = output.split('\n')
    lines.pop(0)
    setting = dict()
    for l in lines:
        r = l.split(":")
        if r[0].strip(" ").strip("\n") == 'data_units_written':
            dev_ex = r[1].strip(" ").strip("\n")
            setting.setdefault("data_units_written", commaInt(dev_ex))

        if r[0].strip(" ").strip("\n") == 'media_errors':
            dev_ex = r[1].strip(" ").strip("\n")
            setting.setdefault("media_errors", commaInt(dev_ex))

        if r[0].strip(" ").strip("\n") == 'host_write_commands':
            dev_ex = r[1].strip(" ").strip("\n")
            setting.setdefault("host_write_commands", commaInt(dev_ex))

    return setting


def crawl_exd():
    try:
        print("check --1")
        disk_counters = psutil.disk_io_counters(perdisk=True)
        for device_name in disk_counters:
            m0 = re.match("^nvme(.*)", device_name)
            if m0:
                meta = dffnvme(device_name)
                print(f'Disk Health - {device_name}: {meta.get("host_write_commands")} b')

        print("check --3")
    except OSError as e:
        print(
            u'Caught exception when crawling disk I/O counters: {0}'.format(e))


print("before __name__ guard")
if __name__ == '__main__':
    crawl_exd()

print("after __name__ guard")
