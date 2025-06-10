from .T_imports import *
from .T_CDLL import *


class LockMe():
    def __init__(self, id, exe):
        self.exe=exe
        self.id=id
        self.__init_set__()
    def __init_set__(self):
        self.hWnd=False
        self.temp=os.getenv("temp")
        self.__python_suffix__=["py", "pyw", "pyc", "pyz", "pyi"]
        self.__python_exe__=["python.exe", "pythonw.exe"]
        self.__exec_suffix__=["exe"]
        self.LockName=f"Lock_{self.id}_[{os.getpid()}].lock"
        self.LockReName=f"Lock_{self.id}_"+r"\[(\d+)\].lock"
    def SearchLockWindow(self, lst, mat):
        result = []
        for s in lst:
            if (_ := re.match(mat, s)): 
                result.append(_.group(1))
        return result
    def SearchLockWindowWithDict(self, lst, mat, key):
        result = []
        for s in lst:
            if (_ := re.match(mat, s["name"])):
                result.append(s[key] if key else s)
        return result
    def IsOtherLock(self):
        bs=0
        if self.IsSelfLock(): bs=1
        SLF=self.SearchLockWindow(self.GetAllWindowInfo("listname"), self.LockReName)
        return len(SLF) > bs
    def GetOtherLockPid(self):
        return self.SearchLockWindowWithDict(self.GetAllWindowInfo("dict"), self.LockReName, "pid")
    def IsSelfLock(self):
        return user32.IsWindow(self.hWnd)
    def lock(self):
        if self.IsOtherLock():
            os._exit(0)
        else:
            try:
                self.CHW(self.LockName)
            except:
                print("WINDOW LOCK ERROR, BUT WE DON'T KILL SELF")
    def CHW(self, title):
        def WndProc(hWnd, msg, wParam, lParam):
            if msg == WM_DESTROY:
                user32.PostQuitMessage(0)
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        def _create_window():
            wc = WNDCLASSW()
            wc.style = CS_HREDRAW | CS_VREDRAW
            wc.lpfnWndProc = WNDPROC(WndProc)
            wc.hInstance = kernel32.GetModuleHandleW(None)
            wc.hCursor = user32.LoadCursorW(None, IDC_ARROW)
            wc.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
            wc.lpszClassName = ctypes.c_wchar_p("HiddenWindowClass")
            class_atom = user32.RegisterClassW(ctypes.byref(wc))
            if class_atom == 0: return False
            self.hWnd = user32.CreateWindowExW(0, wc.lpszClassName, ctypes.c_wchar_p(title),
                WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
                300, 200,
                None, None, wc.hInstance, None
            )
            if not self.hWnd: return False
            user32.ShowWindow(self.hWnd, SW_HIDE)
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        thread = threading.Thread(target=_create_window)
        thread.start()
    def unlock(self):
        if self.IsSelfLock():
            if user32.IsWindow(self.hWnd):
                user32.SendMessageW(self.hWnd, 0x0010, 0, 0)
    def GetAllWindowInfo(self, mod="dict"):
        l = []
        def EnumWindowsProc(hwnd, lParam):
            title_length = user32.GetWindowTextLengthW(hwnd)
            if title_length > 0:
                title = ctypes.create_unicode_buffer(title_length + 1)
                user32.GetWindowTextW(hwnd, title, title_length + 1)
                pid = ctypes.wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if mod == "dict":
                    try:
                        process = psutil.Process(pid.value)
                        exe_path = process.exe()
                        l.append({"name": title.value, "pid": pid.value, "exe": exe_path})
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                if mod == "listname":
                    l.append(title.value)
            return True
        user32.EnumWindows(WNDENUMPROC(EnumWindowsProc), 0)
        return l