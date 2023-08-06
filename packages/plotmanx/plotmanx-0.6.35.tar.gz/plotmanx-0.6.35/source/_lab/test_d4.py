import re

import psutil


def crawl_disk_io_counters():
    try:

        print("check --1")
        disk_counters = psutil.disk_io_counters(perdisk=True)
        print(disk_counters)
        for device_name in disk_counters:
            m0 = re.match("^nvme(.*)$", device_name)
            if m0:
                counters = disk_counters[device_name]
                curr_counters = [
                    counters.read_count,
                    counters.write_count,
                    counters.read_bytes,
                    counters.write_bytes
                ]

                mbpersec = counters.write_bytes / 1024 / 1024

                print(f'Disk I/O counters - {device_name}: {mbpersec} mb/s')
            # yield (device_name, curr_counters)

        print("check --3")
    except OSError as e:
        print(
            u'Caught exception when crawling disk I/O counters: {0}'.format(e))


print("before __name__ guard")
if __name__ == '__main__':
    print("check --v")
    crawl_disk_io_counters()

print("after __name__ guard")
