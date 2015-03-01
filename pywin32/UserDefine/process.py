from ctypes import *
import win32api
import win32con
import win32process

psapi = windll.psapi
kernel = windll.kernel32
Advapi32 = windll.Advapi32

def GetModuleName(hProcess, hModule):
    modname = c_buffer(256)
    psapi.GetModuleBaseNameA(hProcess, hModule, modname, sizeof(modname))
    return "".join([i for i in modname if i != '\x00'])

def EnumProcesses():
    arr = c_ulong * 256
    lpidProcess = arr()
    cb = sizeof(lpidProcess)
    cbNeeded = c_ulong()
    hModule = c_ulong()
    count = c_ulong()
    PROCESS_VM_READ = 0x0010

    # Call Enumprocesses to get hold of process id's
    psapi.EnumProcesses(byref(lpidProcess),
                        cb,
                        byref(cbNeeded))

    #Number of processes returned
    nReturned = cbNeeded.value / sizeof(c_ulong())

    pidProcess = [i for i in lpidProcess][:nReturned]

    for pid in pidProcess:

        #Get handle to the process based on PID
        hProcess = kernel.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                                      False, pid)
        if hProcess:
            psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            yield pid, GetModuleName(hProcess, hModule.value)
            kernel.CloseHandle(hProcess)

class LUID(Structure):
    _fields_ = [('LowPart',c_ulong),
                ('HighPart', c_long)]

def LookupPrivilegeValue(SystemName, Name):
    luid = LUID()
    Advapi32 = windll.LoadLibrary("Advapi32")
    Advapi32.LookupPrivilegeNameA(SystemName, Name, pointer(luid))
    print luid.LowPart
    return luid

class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [('Luid', LUID),
                ('Attributes', c_ulong),
    ]

class TOKEN_PRIVILEGES(Structure):
    _fields_ = [('PrivilegeCount', c_ulong),
                ('Privileges', LUID_AND_ATTRIBUTES)]