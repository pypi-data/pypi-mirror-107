package main

import (
	"copop/pkg"
	"fmt"
	"io"
	"log"
	"math/big"
	"math/rand"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"
)

var BUFFERSIZE int64
var markTime int64

func ccoyc(src, dst string, BUFFERSIZE int64) error {
	sourceFileStat, err := os.Stat(src)
	if err != nil {
		return err
	}

	if !sourceFileStat.Mode().IsRegular() {
		return fmt.Errorf("%s is not a regular file.", src)
	}

	source, err := os.Open(src)
	if err != nil {
		return err
	}
	defer source.Close()

	ff, err := source.Stat()
	if err != nil {
		return err
	}

	_, err = os.Stat(dst)
	if err == nil {
		return fmt.Errorf("File %s already exists.", dst)
	}

	destination, err := os.Create(dst)
	if err != nil {
		return err
	}

	defer destination.Close()

	if err != nil {
		panic(err)
	}

	total := ff.Size()
	buf := make([]byte, BUFFERSIZE)
	buffin := 0
	for {
		n, err := source.Read(buf)
		if err != nil && err != io.EOF {
			return err
		}

		if n == 0 || err == io.EOF {
			//finish ccoycing then the next
			break
		}

		bn, err := destination.Write(buf[:n])

		if err != nil {
			return err
		}

		if time.Now().Unix()-markTime > 60 {
			markTime = time.Now().Unix()
			buffin = buffin + bn
			percent := float64(buffin) / float64(total) * 100
			nowcc := big.NewFloat(percent).SetPrec(3).String()
			Logf("Now:|%6d|%6s %%|\n", buffin, nowcc)
		}
	}
	return err
}

func blocktransfer(source, destination string) {
	BUFFERSIZE, err := strconv.ParseInt(os.Args[3], 10, 64)
	if err != nil {
		Logf("Invalid buffer size: %q\n", err)
		return
	}
	Logf("Copying %s to %s\n", source, destination)
	result := ccoyc(source, destination, BUFFERSIZE)
	if result != nil {
		Logf("File copying failed: %q\n", err)
	} else {
		Logf("File moving file done: %s\n", destination)
	}
}
func sk_open(src_path string) (*pkg.KVStore, error) {
	return pkg.SKVOpen(fmt.Sprintf("%s/writeLock.db", src_path))
}
func mark(sourceDir, filename, destinationDir string, lock bool) {
	store, err := sk_open(sourceDir)
	if err != nil {
		Logf("store 1 err %v", err)
		return
	}
	defer store.Close()
	if lock {
		// put: encodes value with gob and updates the boltdb
		err = store.Put(filename, destinationDir)
	} else {
		// delete: seeks in boltdb and deletes the record
		err = store.Delete(filename)
	}
	if err != nil {
		Logf("store err %v", err)
		return
	}
}

func isLock(sourceDir, filename string) bool {
	var info string
	store, err := sk_open(sourceDir)
	if err != nil {
		return false
	}
	defer store.Close()
	// get: fetches from boltdb and does gob decode
	err = store.Get(filename, &info)
	if err == pkg.ErrNotFound {
		return false
	}
	if &info != nil {
		// busy in use
		return true
	} else {
		return false
	}
}
func isStop(sourceDir string) bool {
	var enabled bool
	store, err := sk_open(sourceDir)
	if err != nil {
		return false
	}
	defer store.Close()
	// get: fetches from boltdb and does gob decode
	err = store.Get("updateStop", &enabled)
	if err == pkg.ErrNotFound {
		err = store.Put("updateStop", false)
		return false
	}
	return enabled
}
func setStop(sdir string, ac bool) {
	store, err := sk_open(sdir)
	if err != nil {
		return
	}
	defer store.Close()
	err = store.Put("updateStop", ac)
}
func Log(s string) {
	var optionalLogFile = ""

	if len(os.Args) == 5 {
		optionalLogFile = os.Args[4]
	} else {
		optionalLogFile = "farm_plot.log"
	}

	f, err := os.OpenFile(optionalLogFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer f.Close()
	wrt := io.MultiWriter(os.Stdout, f)
	//nowExt := time.Now()
	log.SetOutput(wrt)
	log.Println(fmt.Sprintf("%s", s))
}

func Logf(format string, a ...interface{}) {
	Log(fmt.Sprintf(format, a...))
}

var KB = uint64(1024)

func main() {
	var wg sync.WaitGroup
	runtime.GOMAXPROCS(4)
	// pid, _, _ := syscall.Syscall(syscall.SYS_GETPID, 0, 0, 0)
	pid := syscall.Getpid()
	fmt.Println("process id: ", pid)
	syscall.Setpriority(syscall.PRIO_PROCESS, int(pid), 2)
	if len(os.Args) < 4 {
		fmt.Printf("usage: %s source destination BUFFERSIZE logfile(optional) \n", filepath.Base(os.Args[0]))
		return
	}

	sourceDir := os.Args[1]
	ra := os.Args[2]
	k := strings.Index(ra, ",")
	destinationDir := ""

	if ra == "update" {
		control := os.Args[3]
		if control == "yes" {
			setStop(sourceDir, true)
			fmt.Println("ok, yes unlock up for the next stop")
			return
		} else if control == "no" {
			setStop(sourceDir, false)
			fmt.Println("ok, unlocked the control is now updated")
			return
		} else {
			fmt.Println("error, update control is not in control")
			return
		}
	} else {
		destinationDir = ra
	}

	if k > -1 {
		Log("exit and done. because there is not yet developed for destination in list yet")
	} else {
		for {
			if isStop(sourceDir) {
				Logf("Complete and stop worker %d", os.Getegid())
				Log("==============================================")
				break
			}
			matches, _ := filepath.Glob(fmt.Sprintf("%s/*.plot", sourceDir))
			Logf("Found plot files %d", len(matches))

			if len(matches) > 0 {
				s := rand.NewSource(time.Now().Unix())
				r := rand.New(s) // initialize local pseudorandom generator
				match := matches[r.Intn(len(matches))]
				if isLock(sourceDir, match) {
					Logf("Working directory is in busy %s, lets wait 10s", match)
					time.Sleep(10 * time.Second)
					continue
				}
				fileinfo, _ := os.Stat(match)
				if fileinfo.Mode().IsRegular() {
					name := fileinfo.Name()
					des := fmt.Sprintf("%s%s", destinationDir, name)
					usage := pkg.NewDiskUsage(destinationDir)

					if usage.Free() > uint64(fileinfo.Size()) {
						mark(sourceDir, match, des, true)
						blocktransfer(match, des)
						wg.Add(1)
						go func() {
							defer wg.Done()
							defer mark(sourceDir, match, des, false)
							err := os.Remove(match)
							if err != nil {
								Logf("Error from removing file: %s %q\n", match, err)
							}
						}()
					} else {
						Log("Warning! There is not enough space...")
						Logf("Free:", usage.Free()/(KB*KB))
						Logf("Available:", usage.Available()/(KB*KB))
						Logf("Size:", usage.Size()/(KB*KB))
						Logf("Used:", usage.Used()/(KB*KB))
						Logf("Usage:", usage.Usage()*100, "%")
						time.Sleep(100 * time.Second)
					}
				}
				time.Sleep(5 * time.Second)
			} else {
				time.Sleep(50 * time.Second)
			}
		}
	}
	wg.Wait()
}
