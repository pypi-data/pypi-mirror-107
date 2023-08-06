import importlib
import importlib.resources
import os
import re
import socket
import time
from datetime import datetime
from shutil import copyfile
from subprocess import Popen, PIPE

import pkg_resources

from .. import resources as plotman_resources
from ..configuration import get_path

statement = 'End : {}, IO File {}'


def writeFile(content, filename):
    fo = open(filename, "w")
    fo.write(content)
    fo.close()
    print(statement.format(time.ctime(), filename))


class YamlGen:
    setting_yaml = """
    # worked for the host {host}
    # plotman version {ver}
    # last update {date}
    
    user_interface:
            use_stty_size: True
    directories:
            log: /home/ipant/.chia/mainnet
            tmp:
    {list_temp}
            {tmp2_content}
            dst:
    {list_dst}
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
            tmpdir_max_jobs: 45
            global_max_jobs: 90
            global_stagger_m: [12,18]
            polling_time_s: 30
            parallel: 6

    plotting:
            k: 32
            e: True              # Use -e plotting option
            n_threads: 2         # Threads per job
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

    def genTempFolder(self, d: str) -> str:
        return "                - {}/temp".format(d)

    def genDstFolder(self, d: str) -> str:
        return "                - {}/chiaFinalData".format(d)

    def temp2Hx(self, d: str) -> str:
        return "tmp2: {}".format(d)

    def __init__(self):
        self.tmp_list = []
        self.dst_list = []
        self.device_dst_list = []
        self.device_list = []

    def discoverDevices(self):
        df = Popen(["df", "-hT"], stdout=PIPE)
        output = df.communicate()[0]
        listdevice = output.split("\n")
        m = 0
        tmpnvmede = []
        nfsde = []
        for h in listdevice:
            if m > 0:
                device, type, size, used, available, percent, mountpoint = h.split()
                # if that is nvme ssd device we will take it as temp folder
                h = re.match('^\/dev\/md(\d+)', device)
                if h:
                    tmpnvmede.append(mountpoint)

                if type == "nfs4":
                    nfsde.append(mountpoint)

            m += 1

        self.device_list = tmpnvmede
        self.device_dst_list = nfsde

    def generateDummpy(self) -> None:
        if os.path.isfile(get_path()):
            overwrite = None
            while overwrite not in {"y", "n"}:
                overwrite = input(
                    f"A 'plotman.yaml' file already exists at the default location: '{get_path()}' \n\n"
                    "\tInput 'y' to overwrite existing file, or 'n' to exit without overwrite."
                ).lower()

                if overwrite == 'n':
                    print("\nExited without overrwriting file")
                    return

        # Copy the default plotman.yaml (packaged in plotman/resources/) to the user's config file path,
        # creating the parent plotman file/directory if it does not yet exist
        with importlib.resources.path(plotman_resources, "plotman.yaml") as default_config:
            config_dir = os.path.dirname(get_path())
            os.makedirs(config_dir, exist_ok=True)
            copyfile(default_config, get_path())
            print(f"\nWrote default plotman.yaml to: {get_path()}")
            return

    def ensureFolderExist(self, listp: list):
        for d in listp:
            Popen(["mkdir", "-p", d], stdout=PIPE)

    def finalized(self) -> None:
        log_file_time = datetime.strptime('Sun Apr  4 19:00:50 2021', '%a %b  %d %H:%M:%S %Y')
        version_code = pkg_resources.get_distribution('plotmanx')

        for mountpoint in self.device_list:
            self.tmp_list.append(self.genTempFolder(mountpoint))

        for mountptdst in self.device_dst_list:
            self.dst_list.append(self.genDstFolder(mountptdst))

        self.ensureFolderExist(self.tmp_list)

        self.ensureFolderExist(self.dst_list)

        k = self.setting_yaml.format(
            list_dst="\n".join(self.dst_list),
            list_temp="\n".join(self.tmp_list),
            tmp2_content=self.temp2Hx(self.tmp_list[0]),
            ver=version_code,
            date=log_file_time,
            host=socket.gethostname()
        )
        writeFile(k, get_path())
        print("==================")
        print(k)
        print("==================")
