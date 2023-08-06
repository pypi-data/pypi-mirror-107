from source.plotmanx.analyze.pri import LogFile

print("before __name__ guard")
if __name__ == '__main__':
    l = LogFile("test_Data_4.log")
    l.init_logfile()
    print("{:.3g}%".format(l.getProgressPercentage))
    print("read failure:")
    print(l.failure_read)
    print("write failure")
    print(l.disk_confirm)
    print("phase")
    print(l.getPhase)
print("after __name__ guard")
