from .T_imports import *
from .T_SomeThingError import SomeThingError, SomeThingErrorList
from .T_CDLL import *


class AdministratorMode:
    def __init__(self): pass
    def nsudo_elevate(self, argv=sys.argv, target_process="winlogon.exe", logon_flags=LOGON_WITH_PROFILE, token_access=TOKEN_ALL_ACCESS, enable_debug_priv=True):
        _=NsudoSystemProcessRunner(" ".join(argv), target_process=target_process, logon_flags=logon_flags, token_access=token_access, enable_debug_priv=enable_debug_priv)
        return _.Run()
    def _ctypes_elevate(self, show_console=False, argv=sys.argv, encoding="UTF-8"):
        params = ShellExecuteInfo(
            fMask=0x00000040,  # SEE_MASK_NOCLOSEPROCESS
            hwnd=None,
            lpVerb=b'runas',
            lpFile=subprocess.list2cmdline([argv[0]]).encode(encoding),
            lpParameters=(subprocess.list2cmdline(argv[1:]).encode(encoding) if len(argv) > 1 else None),
            nShow=0 if not show_console else 1  # 0=SW_HIDE, 1=SW_SHOWNORMAL
        )
        if not shell32.ShellExecuteExA(ctypes.byref(params)):
            return None
        pid = kernel32.GetProcessId(params.hProcess)
        kernel32.CloseHandle(params.hProcess)
        return pid
    def IsUserAnAdmin(self):
        return shell32.IsUserAnAdmin()
    def IsUserAnSystemAdmin(self):
        return str(os.popen("whoami").read()).lower().count("system") >= 1
    def Is64BitSystem(self):
        return sys.maxsize > 2**32


class NsudoSystemProcessRunner:
    def __init__(self, 
                 command_line: str,
                 target_process: str = "winlogon.exe",
                 logon_flags: int = LOGON_WITH_PROFILE,
                 token_access: int = TOKEN_ALL_ACCESS,
                 enable_debug_priv: bool = True):
        self.error_map = {
            -5: "拒绝访问（需要管理员权限）",
            -2: "文件未找到",
            -1168: "目标进程不存在",
            -1314: "权限不足",
            -1008: "无可用令牌",
            -0xFFFF: "未知错误"
        }
        self.command_line = command_line
        self.target_process = target_process.lower()
        self.logon_flags = logon_flags
        self.token_access = token_access
        self.enable_debug_priv = enable_debug_priv
        self._handles = []
    def Run(self) -> int:
        try:
            if self.enable_debug_priv:
                if not self._enable_debug_privilege():
                    return -self._get_last_error()
            pid = self._find_target_process()
            if pid <= 0:
                return pid
            h_token = self._get_process_token(pid)
            if not h_token:
                return -self._get_last_error()
            duplicated_token = self._duplicate_token(h_token)
            if not duplicated_token:
                return -self._get_last_error()
            new_pid = self._create_process_with_token(duplicated_token)
            if new_pid <= 0:
                return new_pid
            return new_pid
        finally:
            self._cleanup_handles()
    def _enable_debug_privilege(self) -> bool:
        h_token = ctypes.wintypes.HANDLE()
        if not OpenProcessToken(GetCurrentProcess(), 
                               TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                               ctypes.byref(h_token)):
            return False
        try:
            luid = self._lookup_privilege_value(SE_DEBUG_PRIVILEGE)
            if luid is None:
                return False
            return self._adjust_token_privileges(h_token, luid)
        finally:
            CloseHandle(h_token)
    def _lookup_privilege_value(self, name: str) -> typing.Optional[LUID]:
        luid = LUID()
        if not LookupPrivilegeValueW(None, name, ctypes.byref(luid)):
            return None
        return luid
    def _adjust_token_privileges(self, token: ctypes.wintypes.HANDLE, luid: LUID) -> bool:
        tp = TOKEN_PRIVILEGES()
        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
        return bool(AdjustTokenPrivileges(
            token,
            False,
            ctypes.byref(tp),
            0,
            None,
            None
        ))
    def _find_target_process(self) -> int:
        h_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if h_snapshot == ctypes.wintypes.HANDLE(-1):
            return -self._get_last_error()
        try:
            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
            if not Process32FirstW(h_snapshot, ctypes.byref(pe32)):
                return -self._get_last_error()
            while True:
                if pe32.szExeFile.lower() == self.target_process:
                    return pe32.th32ProcessID
                if not Process32NextW(h_snapshot, ctypes.byref(pe32)):
                    break
            self._set_last_error(ERROR_NOT_FOUND)
            return -ERROR_NOT_FOUND
        finally:
            CloseHandle(h_snapshot)
    def _get_process_token(self, pid: int) -> typing.Optional[ctypes.wintypes.HANDLE]:
        h_process = OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        if not h_process:
            return None
        try:
            h_token = ctypes.wintypes.HANDLE()
            access = TOKEN_DUPLICATE | TOKEN_QUERY | TOKEN_ASSIGN_PRIMARY
            if not OpenProcessToken(h_process, access, ctypes.byref(h_token)):
                return None
            return h_token
        finally:
            CloseHandle(h_process)
    def _duplicate_token(self, src_token: ctypes.wintypes.HANDLE) -> typing.Optional[ctypes.wintypes.HANDLE]:
        h_duplicated = ctypes.wintypes.HANDLE()
        if not DuplicateTokenEx(
            src_token,
            self.token_access,
            None,
            SecurityImpersonation,
            TokenPrimary,
            ctypes.byref(h_duplicated)
        ):
            return None
        return h_duplicated
    def _create_process_with_token(self, token: ctypes.wintypes.HANDLE) -> int:
        startup_info = STARTUPINFOW()
        startup_info.cb = ctypes.sizeof(STARTUPINFOW)
        process_info = PROCESS_INFORMATION()
        if not CreateProcessWithTokenW(
            token,
            self.logon_flags,
            None,
            self.command_line,
            0,
            None,
            None,
            ctypes.byref(startup_info),
            ctypes.byref(process_info)
        ):
            return -self._get_last_error()
        CloseHandle(process_info.hProcess)
        CloseHandle(process_info.hThread)
        return process_info.dwProcessId
    def _cleanup_handles(self):
        while self._handles:
            handle = self._handles.pop()
            if handle:
                CloseHandle(handle)
    def _get_last_error(self) -> int:
        return GetLastError()
    def _set_last_error(self, code: int):
        ctypes.windll.kernel32.SetLastError(code)