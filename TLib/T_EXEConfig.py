from .T_imports import *
from .T_FIO import FIO
from .T_GodKeys import GodKeys


class EXEConfig:
    def __init__(self, master: 'Termination4.Termination', FilePath, FileBytes=None):
        self.master=master
        self.FilePath=FilePath
        self.FileBytes=FileBytes
        self.__init_values__()
    def __init_values__(self):
        self.GodKeys=GodKeys(b"EXMODECONFIGKEYS"*2)
        try:
            try: self.File=FIO.openr(self.FilePath, 2)
            except: self.File=self.FileBytes
            self.FileBytes=self._Search(self.File, b"EXMODECONFIGSTART", b"EXMODECONFIGEND")
            self.Config=self.GodKeys.decrypt(self.FileBytes)
        except: return
    def Is(self):
        return hasattr(self, "Config") and self.Config and dict == type(self.Config)
    def GetConfig(self, key):
        try:
            if key in self.Config:
                return self.Config[key]
        except: pass
        return
    def _Search(self, b, s, e):
        m = re.compile(s+rb"(.*)"+e).search(b)
        if not m: return False
        return m.group(1)