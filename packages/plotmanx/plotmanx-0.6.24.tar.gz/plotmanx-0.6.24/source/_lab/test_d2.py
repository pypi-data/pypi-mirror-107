import re
from subprocess import Popen, PIPE

print("before __name__ guard")
if __name__ == '__main__':

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

    print(nfsde)
print("after __name__ guard")
