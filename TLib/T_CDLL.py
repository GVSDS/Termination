from .T_imports import *


user32 = ctypes.WinDLL('user32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
shell32 = ctypes.WinDLL('shell32', use_last_error=True)
GW_HWNDNEXT = 2
MAX_PATH = 260
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001
IDC_ARROW = 32512
IDI_APPLICATION = 32512
WS_OVERLAPPEDWINDOW = 0x00CF0000
SW_HIDE = 0
WM_DESTROY = 0x0002
CW_USEDEFAULT = -1
WNDPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.LPARAM, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", ctypes.wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", ctypes.wintypes.HINSTANCE),
        ("hIcon", ctypes.wintypes.HANDLE),
        ("hCursor", ctypes.wintypes.HANDLE),
        ("hbrBackground", ctypes.wintypes.HANDLE),
        ("lpszMenuName", ctypes.wintypes.LPCWSTR),
        ("lpszClassName", ctypes.wintypes.LPCWSTR)
    ]
class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize',       ctypes.wintypes.DWORD),
        ('fMask',        ctypes.c_ulong),
        ('hwnd',         ctypes.wintypes.HWND),
        ('lpVerb',       ctypes.c_char_p),
        ('lpFile',       ctypes.c_char_p),
        ('lpParameters', ctypes.c_char_p),
        ('lpDirectory',  ctypes.c_char_p),
        ('nShow',        ctypes.c_int),
        ('hInstApp',     ctypes.wintypes.HINSTANCE),
        ('lpIDList',     ctypes.c_void_p),
        ('lpClass',      ctypes.c_char_p),
        ('hKeyClass',    ctypes.wintypes.HKEY),
        ('dwHotKey',     ctypes.wintypes.DWORD),
        ('hIcon',        ctypes.wintypes.HANDLE),
        ('hProcess',     ctypes.wintypes.HANDLE)
    ]
    def __init__(self, **kw):
        super(ShellExecuteInfo, self).__init__()
        self.cbSize = ctypes.sizeof(self)
        for field_name, field_value in kw.items():
            setattr(self, field_name, field_value)
'''class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize',       ctypes.wintypes.DWORD),
        ('fMask',        ctypes.c_ulong),
        ('hwnd',         ctypes.wintypes.HWND),
        ('lpVerb',       ctypes.c_char_p),
        ('lpFile',       ctypes.c_char_p),
        ('lpParameters', ctypes.c_char_p),
        ('lpDirectory',  ctypes.c_char_p),
        ('nShow',        ctypes.c_int),
        ('hInstApp',     ctypes.wintypes.HINSTANCE),
        ('lpIDList',     ctypes.c_void_p),
        ('lpClass',      ctypes.c_char_p),
        ('hKeyClass',    ctypes.wintypes.HKEY),
        ('dwHotKey',     ctypes.wintypes.DWORD),
        ('hIcon',        ctypes.wintypes.HANDLE),
        ('hProcess',     ctypes.wintypes.HANDLE)
    ]

    def __init__(self, **kw):
        super(ShellExecuteInfo, self).__init__()
        self.cbSize = ctypes.sizeof(self)
        for field_name, field_value in kw.items():
            setattr(self, field_name, field_value)'''
user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
user32.RegisterClassW.restype = ctypes.wintypes.ATOM
user32.CreateWindowExW.argtypes = [
    ctypes.wintypes.DWORD, ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.wintypes.HWND, ctypes.wintypes.HMENU, ctypes.wintypes.HINSTANCE, ctypes.wintypes.LPVOID
]
user32.CreateWindowExW.restype = ctypes.wintypes.HWND
user32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = ctypes.wintypes.BOOL
user32.GetMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG), ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.UINT]
user32.GetMessageW.restype = ctypes.wintypes.BOOL
user32.TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]
user32.TranslateMessage.restype = ctypes.wintypes.BOOL
user32.DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]
user32.DispatchMessageW.restype = ctypes.wintypes.LPARAM
user32.DefWindowProcW.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]
user32.DefWindowProcW.restype = ctypes.wintypes.LPARAM
shell32.ShellExecuteExA.argtypes = (ctypes.POINTER(ShellExecuteInfo), )
shell32.ShellExecuteExA.restype = ctypes.wintypes.BOOL
kernel32.WaitForSingleObject.argtypes = (ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD)
kernel32.WaitForSingleObject.restype = ctypes.wintypes.DWORD
kernel32.CloseHandle.argtypes = (ctypes.wintypes.HANDLE, )
kernel32.CloseHandle.restype = ctypes.wintypes.BOOL
CopyFileW = kernel32.CopyFileW
CopyFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool]
CopyFileW.restype = ctypes.c_bool

def CopyFile(source_path, destination_path):
    result = CopyFileW(source_path, destination_path, False)
    if result:
        return True
    else:
        error_code = kernel32.GetLastError()
        raise IOError(f"CopyFileW bad by error code {error_code}")

# ----- ADMIN -----
class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", ctypes.wintypes.DWORD),
        ("lpSecurityDescriptor", ctypes.wintypes.LPVOID),
        ("bInheritHandle", ctypes.wintypes.BOOL)
    ]

class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.wintypes.DWORD),
        ("HighPart", ctypes.wintypes.LONG)
    ]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", ctypes.wintypes.DWORD)
    ]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", ctypes.wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1)
    ]

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', ctypes.wintypes.DWORD),
        ('cntUsage', ctypes.wintypes.DWORD),
        ('th32ProcessID', ctypes.wintypes.DWORD),
        ('th32DefaultHeapID', ctypes.c_size_t),
        ('th32ModuleID', ctypes.wintypes.DWORD),
        ('cntThreads', ctypes.wintypes.DWORD),
        ('th32ParentProcessID', ctypes.wintypes.DWORD),
        ('pcPriClassBase', ctypes.wintypes.LONG),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('szExeFile', ctypes.c_wchar * 260)
    ]

class STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.wintypes.DWORD),
        ("lpReserved", ctypes.wintypes.LPWSTR),
        ("lpDesktop", ctypes.wintypes.LPWSTR),
        ("lpTitle", ctypes.wintypes.LPWSTR),
        ("dwX", ctypes.wintypes.DWORD),
        ("dwY", ctypes.wintypes.DWORD),
        ("dwXSize", ctypes.wintypes.DWORD),
        ("dwYSize", ctypes.wintypes.DWORD),
        ("dwXCountChars", ctypes.wintypes.DWORD),
        ("dwYCountChars", ctypes.wintypes.DWORD),
        ("dwFillAttribute", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("wShowWindow", ctypes.wintypes.WORD),
        ("cbReserved2", ctypes.wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
        ("hStdInput", ctypes.wintypes.HANDLE),
        ("hStdOutput", ctypes.wintypes.HANDLE),
        ("hStdError", ctypes.wintypes.HANDLE)
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.wintypes.HANDLE),
        ("hThread", ctypes.wintypes.HANDLE),
        ("dwProcessId", ctypes.wintypes.DWORD),
        ("dwThreadId", ctypes.wintypes.DWORD)
    ]

PROCESS_QUERY_INFORMATION = 0x0400
TOKEN_DUPLICATE = 0x0002
TOKEN_QUERY = 0x0008
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_ALL_ACCESS = 0xF01FF
SecurityImpersonation = 2
TokenPrimary = 1
LOGON_WITH_PROFILE = 0x00000001
SE_DEBUG_PRIVILEGE = "SeDebugPrivilege"
SE_PRIVILEGE_ENABLED = 0x00000002
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
TH32CS_SNAPPROCESS = 0x00000002
ERROR_NO_TOKEN = 1008
ERROR_NOT_FOUND = 1168

# OpenProcessToken
OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.HANDLE)]
OpenProcessToken.restype = ctypes.wintypes.BOOL

# LookupPrivilegeValueW
LookupPrivilegeValueW = advapi32.LookupPrivilegeValueW
LookupPrivilegeValueW.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR, ctypes.POINTER(LUID)]
LookupPrivilegeValueW.restype = ctypes.wintypes.BOOL

# AdjustTokenPrivileges
AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.BOOL,
    ctypes.POINTER(TOKEN_PRIVILEGES),
    ctypes.wintypes.DWORD,
    ctypes.POINTER(TOKEN_PRIVILEGES),
    ctypes.POINTER(ctypes.wintypes.DWORD)
]
AdjustTokenPrivileges.restype = ctypes.wintypes.BOOL

# DuplicateTokenEx
DuplicateTokenEx = advapi32.DuplicateTokenEx
DuplicateTokenEx.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.POINTER(SECURITY_ATTRIBUTES),
    ctypes.wintypes.INT,
    ctypes.wintypes.INT,
    ctypes.POINTER(ctypes.wintypes.HANDLE)
]
DuplicateTokenEx.restype = ctypes.wintypes.BOOL

# CreateProcessWithTokenW
CreateProcessWithTokenW = advapi32.CreateProcessWithTokenW
CreateProcessWithTokenW.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.LPVOID,
    ctypes.wintypes.LPCWSTR,
    ctypes.POINTER(STARTUPINFOW),
    ctypes.POINTER(PROCESS_INFORMATION)
]
CreateProcessWithTokenW.restype = ctypes.wintypes.BOOL

# OpenProcess
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
OpenProcess.restype = ctypes.wintypes.HANDLE

# CloseHandle
CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
CloseHandle.restype = ctypes.wintypes.BOOL

# CreateToolhelp32Snapshot
CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
CreateToolhelp32Snapshot.restype = ctypes.wintypes.HANDLE

# Process32FirstW
Process32FirstW = kernel32.Process32FirstW
Process32FirstW.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
Process32FirstW.restype = ctypes.wintypes.BOOL

# Process32NextW
Process32NextW = kernel32.Process32NextW
Process32NextW.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
Process32NextW.restype = ctypes.wintypes.BOOL

# GetCurrentProcess
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = ctypes.wintypes.HANDLE

# GetLastError
GetLastError = kernel32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = ctypes.wintypes.DWORD

# ----- KEMOUSE -----
# 定义系统相关类型
"""
ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR)
    ]

class KeybdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.WORD)
    ]

class InputUnion(ctypes.Union):
    _fields_ = [
        ("mi", MouseInput),
        ("ki", KeybdInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("union", InputUnion)
    ]

# 输入类型常量
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

class GrayImage(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

class Point(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int)
    ]
"""

class GrayImage(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

class MatchResult(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("error", ctypes.c_int),
        ("confidence", ctypes.c_double)
    ]

# 定义 Windows 输入结构
class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
    ]

class InputUnion(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("union", InputUnion)
    ]

# 定义常量
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_ABSOLUTE = 0x8000

class DLL(ctypes.CDLL):
    def __init__(self, DLL_Path, mode=ctypes.DEFAULT_MODE, handle=None,
                 use_errno=False,
                 use_last_error=False,
                 winmode=None):
        super().__init__(DLL_Path, mode=mode, handle=handle,
                         use_errno=use_errno,
                         use_last_error=use_last_error,
                         winmode=winmode)

"""
class DLL(ctypes.CDLL):
    def __init__(self, dll_data_or_path, mode=ctypes.DEFAULT_MODE, handle=None,
                 use_errno=False, use_last_error=False, winmode=None):
        
        if isinstance(dll_data_or_path, (bytes, bytearray)):
            # 处理内存中的DLL数据
            import tempfile
            self._temp_file = tempfile.NamedTemporaryFile(suffix='.dll', delete=False)
            self._temp_file.write(dll_data_or_path)
            self._temp_file.close()
            path = self._temp_file.name
            self._is_temp = True
        else:
            # 处理文件路径
            path = dll_data_or_path
            self._is_temp = False
        
        super().__init__(path, mode=mode, handle=handle,
                        use_errno=use_errno,
                        use_last_error=use_last_error,
                        winmode=winmode)
    
    def __del__(self):
        if hasattr(self, '_is_temp') and self._is_temp:
            try:
                os.unlink(self._temp_file.name)
            except:
                pass"""