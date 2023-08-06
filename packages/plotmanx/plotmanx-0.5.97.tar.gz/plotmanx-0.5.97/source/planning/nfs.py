# !/usr/bin/env python3

import os

import xlsxwriter

servers = [61, 62, 63, 64, 66, 67, 68, 69, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
storage1 = [236, 237, 238, 239, 240, 241, 242, 243]
storage2 = [101, 102, 103, 104, 105, 106, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130]
dst = "/Users/hesdx/Documents/ipfs/deplotplot/workersv1"

c = 0

tyaml = """

user_interface:
        use_stty_size: True
directories:
        log: /home/ipant/.chia/mainnet
        tmp:
                - /mnt/local/tmp
        tmp2: /mnt/local/tmp

        dst:
{list}
        archive:
                #rsyncd_module: plots
                #rsyncd_path: /plots
                #rsyncd_bwlimit: 80000  # Bandwidth limit in KB/s
                #rsyncd_host: myfarmer
                #rsyncd_user: chia
                #index: 0
scheduling:
        tmpdir_stagger_phase_major: 2
        tmpdir_stagger_phase_minor: 1
        tmpdir_stagger_phase_limit: 6
        tmpdir_max_jobs: 40
        global_max_jobs: 36
        global_stagger_m: [12,18]
        polling_time_s: 30
        parallel: 6
        
plotting:
        k: 32
        e: True              # Use -e plotting option
        n_threads: 4         # Threads per job
        n_buckets: 128       # Number of buckets to split data into
        job_buffer: 32000     # Per job memory
        # If specified, pass through to the -f and -p options.  See CLI reference.
        farmer_pk: 861467df6768932f1c2f3a7c00a70f1e111b22b55de42c497fb93fd398eb4fd4b213f399e0930d265ffdc2b5655f96f5
        pool_pk: 8e211cb1118b95ac9da2f31fd159a74993bfcc8ab72bff79c880227185ba2b1f372b8e829bd99f5796eb4f68e41f30a9

apis:
        api_polling_throttle_s: 5
        port: 19451
        target: "121.29.84.81"
        """

mjob = """

if [ ! -d "{target}" ]; then
    sudo mkdir -p {target}
    echo "mount drive 192.168.10.{worker_id}"
    sudo mount -t nfs 192.168.10.{worker_id}:/minerdata {target} -o nolock
fi

"""
ransfar = """
nohup ./plmo /mnt/local/tmp /mnt/nfs/{foldername}/chiaFinalData/ 50000000 &
"""

upgrade = """

cd ~/chia-blockchain/
wget https://gitee.com/Yang007GG_com/plotman/attach_files/711891/download/nvme_linux_0.4.80.zip && unzip -o nvme_linux_0.4.80.zip 
rm nvme_linux_0.4.80.zip

"""


def filename(k) -> str:
    if k < len(storage1):
        u = storage1[k]
        return "storage{}".format(u)
    else:
        if k < len(storage2):
            p = storage2[k - len(storage1)]
            return "ipant{}".format(p)
        else:
            p1 = storage2[k - len(storage1) - len(storage2)]
            return "ipant{}".format(p1)


def workerID(k) -> str:
    if k < len(storage1):
        u = storage1[k]
        return u
    else:
        if k < len(storage2):
            p = storage2[k - len(storage1)]
            return p
        else:
            p1 = storage2[k - len(storage1) - len(storage2)]
            return p1


def appendx(d) -> str:
    return "                - /mnt/nfs/{}/chiaFinalData".format(d)


def nameFile(formatc, workerID: int) -> any:
    km = formatc.format(workerID)
    file = os.path.join(dst, km)
    return file


def mountdisk(d) -> str:
    return "/mnt/nfs/{}".format(d)


class ExcelSheetGen:
    def __init__(self, basepath: str):
        # Create a workbook and add a worksheet.
        self.workbook = xlsxwriter.Workbook(os.path.join(basepath, 'chiaNodes.xlsx'))
        self.worksheet = self.workbook.add_worksheet()

        # Start from the first cell. Rows and columns are zero indexed.
        self.row = 1
        self.col = 0
        self.worksheet.write(self.row, self.col, "connect cmd")
        self.worksheet.write(self.row, self.col + 1, "worker IP")
        self.worksheet.write(self.row, self.col + 2, "path NFS")
        self.worksheet.write(self.row, self.col + 3, "path NFS")
        self.worksheet.write(self.row, self.col + 4, "path NFS")
        self.row += 1

    def dataEnter(self, wid, workerId, folder1, folder2, folder3):
        wtxt = "W{}".format(wid)
        wkidtxt="192.168.10.{}".format(workerId)
        # Some data we want to write to the worksheet.
        self.worksheet.write(self.row, self.col, wtxt)
        self.worksheet.write(self.row, self.col + 1, wkidtxt)
        self.worksheet.write(self.row, self.col + 2, folder1)
        self.worksheet.write(self.row, self.col + 3, folder2)
        self.worksheet.write(self.row, self.col + 4, folder3)
        self.row += 1

    def endExcel(self):
        # Write a total using a formula.
        # self.worksheet.write(row, 0, 'Total')
        # self.worksheet.write(row, 1, '=SUM(B1:B4)')
        self.workbook.close()


book = ExcelSheetGen(dst)

for i in servers:
    k = list()
    id1 = c * 3
    id2 = c * 3 + 1
    id3 = c * 3 + 2
    d1 = filename(id1)
    d2 = filename(id2)
    d3 = filename(id3)

    k.append(appendx(d1))
    k.append(appendx(d2))
    k.append(appendx(d3))

    s = tyaml.format(list="\n".join(k))
    print("W{} -> worker{} -> {} {} {}".format(c + 1, i, d1, d2, d3))

    with open(nameFile("worker{}.yaml", i), 'w') as f:
        f.write(s)
        f.close()

    with open(nameFile("workerMoverInstall{}.sh", i), 'w') as f:
        f.write("#!/bin/bash\n")
        f.write(mjob.format(target=mountdisk(d1), worker_id=workerID(id1)))
        f.write(mjob.format(target=mountdisk(d2), worker_id=workerID(id2)))
        f.write(mjob.format(target=mountdisk(d3), worker_id=workerID(id3)))
        f.write(ransfar.format(foldername=filename(id1)))
        f.write(ransfar.format(foldername=filename(id2)))
        f.write(ransfar.format(foldername=filename(id3)))
        f.write(upgrade)
        f.close()

    book.dataEnter(c + 1, i, d1, d2, d3)
    print("excel new line")

    c += 1
book.endExcel()
