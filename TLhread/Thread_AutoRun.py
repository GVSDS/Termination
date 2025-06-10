from TLib import *
from TLib.T_imports import *


class AutoRunSetup(T_Process.TProcess):
    def Setup(self, master: 'Termination4.Termination'):
        self.master=master
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        self.desc="AutoRun Setup"
        if os.path.abspath(self.master.__file__).lower() != os.path.abspath(self.master.PDir.__need_file__).lower():
            print("AUTORUN: NOT TRUE SIT MODE")
            return -4
        else:
            print("AUTORUN: TRUE SIT MODE Successful")
        if not hasattr(self.master.PDir, "__need_TService__"):
            print("AUTORUN: PDIR ERROR")
            return -5
        else:
            print("AUTORUN: PDIR Sucessful")
        if not (service:=self.master.tpll.IsService(self.master.__service_name__)):
            if not (r:=self.master.tpll.Command([self.master.PDir.__need_TService__, "/install", self.master.PDir.__need_file__])).successtatus():
                print(f"AUTORUN: Bad Install Service : [{r}]")
                return False
            else:
                print("AUTORUN: Install Service Sucessful")
        print(f"AUTORUN: BINPATH {(b:=self.master.tpll.GetServiceBinpath(self.master.__service_name__))} SHLEXSPLIT {(p:=shlex.split(b) if b else False)}")
        if b and p and os.path.abspath(p[-1]).lower() != os.path.abspath(self.master.PDir.__need_file__).lower():
            print(f"AUTORUN: EPATH {os.path.abspath(p[-1]).lower()} | {os.path.abspath(self.master.PDir.__need_file__).lower()}")
            if not (r1:=self.master.tpll.Command([self.master.PDir.__need_TService__, "/uninstall"])).successtatus() or not (
                r2:=self.master.tpll.Command([self.master.PDir.__need_TService__, "/install", self.master.PDir.__need_file__])).successtatus():
                print(f"AUTORUN: Bad Re Service : U[{r1}] I[{r2}]")
            else:
                print("AUTORUN: Re Service Successful")
        if not service or service.status() == "stopped":
            if not (r:=self.master.tpll.WindowsService.StartService(self.master.__service_name__)==True):
                print(f"AUTORUN: Bad Start Service : [{r}]")
            else:
                print("AUTORUN: Start Service Sucessful")
        return True
    def stop(self):
        if (service:=self.master.tpll.IsService(self.master.__service_name__)) and service.status() == "running":
            if not (r:=self.master.tpll.WindowsService.StopService(self.master.__service_name__) == True):
                self.master.TWNT.Updating=False
                return print(f"END THE SERVICE ERROR, PLEASE END THE SERVICE! ERROR: [{r}]")
            else:
                os.system("taskkill /F /IM TService.exe")
                print("[EXIT] End The Service Successful")
                return True
        else:
            print("[EXIT] Service Was Stop")
            return True
    def iswork(self):
        return (service:=self.master.tpll.IsService(self.master.__service_name__)) and service.status() == "running"