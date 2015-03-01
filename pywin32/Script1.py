# coding=gbk
import win32api
import win32con
import win32process
import win32pdh
from ctypes import *
import win32security
import UserDefine.process as apiprocess

psapi = windll.psapi
kernel = windll.kernel32
Advapi32 = windll.Advapi32


def proclist():
    try:
        junk, instances = win32pdh.EnumObjectItems(None, None, object, win32pdh.PERF_DETAIL_WIZARD)
        return instances
    except:
        # raise COMException("Problem getting process list")
        pass


def foo():
    # win32api.ExitWindows(win32con.EWX_FORCE | win32con.EWX_SHUTDOWN)
    try:
        # win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, win32process.GetCurrentProcess())
        processes = win32process.EnumProcesses()
        for process in processes:
            try:
                hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, process)
                if not hProcess:
                    continue
                print 'open %d success' % process
                processModules = win32process.EnumProcessModules(hProcess)
                for processModule in processModules:
                    print 'processModule %d' % processModule
                    # print 'moduleFileName %s' % str(GetModuleFileNameEx(hProcess, processModule))
                    # print 'moduleFileName %s' % ''
                    print 'haha'
            except Exception as e:
                # print 'open %d failed' % process
                continue
                # print processes
    except Exception as e:
        print process
        print e


def procids():
    # each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids = []
    proc_dict = {}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance] = 0
    for instance, max_instances in proc_dict.items():
        for inum in xrange(max_instances + 1):
            hq = win32pdh.OpenQuery()  # initializes the query handle
            path = win32pdh.MakeCounterPath((None, 'process', instance, None, inum, 'ID Process'))
            counter_handle = win32pdh.AddCounter(hq, path)
            win32pdh.CollectQueryData(hq)  # collects data for the counter
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance, str(val)))
            win32pdh.CloseQuery(hq)

    proc_ids.sort()
    return proc_ids


class Pointer(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int),
    ]


class Pointer1(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int),
    ]


class StructPointerTest(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int),
                ('z', Pointer),
                ('a', POINTER(Pointer1)),
    ]


if __name__ == '__main__':
    Advapi32 = windll.LoadLibrary("Advapi32")

    hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, win32api.GetCurrentProcessId());
    hToken = win32security.OpenProcessToken(hProcess, win32con.TOKEN_ADJUST_PRIVILEGES)
    value = apiprocess.LookupPrivilegeValue("", win32con.SE_DEBUG_NAME)
    la = apiprocess.LUID_AND_ATTRIBUTES(value, win32con.SE_PRIVILEGE_ENABLED)
    tpIn = apiprocess.TOKEN_PRIVILEGES(1, la)
    tpOut = apiprocess.TOKEN_PRIVILEGES()
    print dir(hToken), pointer(tpIn)
    Advapi32.LookupPrivilegeNameA.argtypes = [c_ulong, c_bool, POINTER(apiprocess.TOKEN_PRIVILEGES), c_ulong,
                                              POINTER(apiprocess.TOKEN_PRIVILEGES), c_ulong]
    Advapi32.LookupPrivilegeNameA(240, 0, pointer(tpIn), sizeof(tpIn), pointer(tpOut), sizeof(tpOut))

    # lib.test.restype = PO1INTER(StructPointer)
    # p = lib.test()
    # print p.contents.x
    # p = Pointer(1, 2)
    # p1 = Pointer1(1, 2)
    # 获取结构体指针 pointer
    # s = StructPointerTest(1,2, p, pointer(p1))
    #
    # print s.x, s.y
    # pass


