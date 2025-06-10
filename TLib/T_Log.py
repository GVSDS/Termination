from .T_imports import *
from .T_FIO import FIO


class Log():
    def __init__(self, MainName, Echo=True, ErrorCallBack = lambda: None):
        self.MainName=MainName
        self.Echo=Echo
        self.ErrorCallBack=ErrorCallBack
    def error(self, e, n, w=False):
        n=n if n else self.MainName
        p=self.TimeFormat(n, e, "ERROR")
        if self.Echo: print(colorama.Fore.RED, p, colorama.Style.RESET_ALL)
        if w:
            self.ErrorCallBack()
            os._exit(0)
        return p
    def info(self, i, n):
        n=n if n else self.MainName
        p=self.TimeFormat(n, i, "INFO")
        if self.Echo: print(colorama.Fore.WHITE, p, colorama.Style.RESET_ALL)
        return p
    def warning(self, w, n):
        n=n if n else self.MainName
        p=self.TimeFormat(n, w, "WARNING")
        if self.Echo: print(colorama.Fore.YELLOW, p, colorama.Style.RESET_ALL)
        return p
    def debug(self, d, n):
        n=n if n else self.MainName
        p=self.TimeFormat(n, d, "DEBUG")
        if self.Echo: print(colorama.Fore.LIGHTYELLOW_EX, p, colorama.Style.RESET_ALL)
        return p
    def success(self, s, n):
        n=n if n else self.MainName
        p=self.TimeFormat(n, s, "SUCCESS")
        if self.Echo: print(colorama.Fore.GREEN, p, colorama.Style.RESET_ALL)
        return p
    def TimeFormat(self, ch, s, i):
        return f"{time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())} [{ch}] [{i}]: {str(s)}"
    def TimeFormatTime(self, t=None):
        return time.strftime(t if t else "%Y-%m-%d-%H-%M-%S", time.localtime())
class LogCher():
    def __init__(self, Master: Log, Name: str):
        self.Master=Master
        self.Name=Name
    def error(self, e, w=False):
        return self.Master.error(e, self.Name, w)
    def info(self, i):
        return self.Master.info(i, self.Name)
    def warning(self, w):
        return self.Master.warning(w, self.Name)
    def debug(self, d):
        return self.Master.debug(d, self.Name)
    def success(self, s):
        return self.Master.success(s, self.Name)