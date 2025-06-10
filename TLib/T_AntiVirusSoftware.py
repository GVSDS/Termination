from TLib import *
from .T_imports import *
from .T_CDLL import *



class AntiVirusSoftwareTools:
    def __init__(self, KeMouse: 'T_KeMouse.KeMouse', OCRPath: str):
        self.KeMouse=KeMouse
        self.OCRPath=OCRPath
        self.__init_values__()
    def __init_values__(self):
        self.temp=os.getenv("temp")
        self.OCR_Down=os.path.join(self.OCRPath, "Down.png")
        self.OCR_NFTB=os.path.join(self.OCRPath, "NFTB.png")
        self.OCR_AcceptAll=os.path.join(self.OCRPath, "AcceptAll.png")
        self.OCR_AddToBelive=os.path.join(self.OCRPath, "AddToBelive.png")
        self.OCR_CloseBeliveWindow=os.path.join(self.OCRPath, "CloseBeliveWindow.png")
    #def GetWindowsByClass(self, className):
    #    try:
    #        windows = []
    #        def EnumWindowsCallback(hwnd, _):
    #            try: currentClassName = win32gui.GetClassName(hwnd)
    #            except: return False
    #            if currentClassName == className: windows.append(hwnd)
    #            return True
    #        win32gui.EnumWindows(EnumWindowsCallback, None)
    #        return windows
    #    except:
    #        print("GetWindowsByClass Error")
    #        return []
    def GetWindowsByClass(self, className):
        try:
            return win32gui.FindWindow(className, None)
        except Exception as e:
            print(f"GetFirstWindowByClass Error: {e}")
            return None
    def GetWindowCoordinates(self, hwnd):
        try:
            rect = win32gui.GetWindowRect(hwnd)
            left = rect[0]
            top = rect[1]
            right = rect[2]
            bottom = rect[3]
            return left, top, right, bottom
        except:
            return False, False, False, False
    def GetSomeWindow(self, BanTitle, BanName):
        self._r=False
        def enum_callback(hwnd, _):
            if not user32.IsWindowVisible(hwnd):
                return True
            title_length = user32.GetWindowTextLengthW(hwnd)
            if title_length <= 0:
                return True
            title = ctypes.create_unicode_buffer(title_length + 1)
            user32.GetWindowTextW(hwnd, title, title_length + 1)
            pid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            try:
                exe_path = psutil.Process(pid.value).exe()
                title=title.value
                if any(_ in title for _ in BanTitle) or any(_ in exe_path for _ in BanName):
                    self._r={"name": title, "pid": pid.value, "exe": exe_path}
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            return True
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
        return self._r