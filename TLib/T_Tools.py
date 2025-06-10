from .T_imports import *


@staticmethod
def RegTaskmgrDis():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False
@staticmethod
def RegEditDis():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False
@staticmethod
def RegBgDis():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, r"c:\\" )
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False

@staticmethod
def RegTaskmgrEnable():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False
@staticmethod
def RegEditEnable():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False
@staticmethod
def RegBgEnable():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.DeleteValue(key, "Wallpaper")
        winreg.DeleteValue(key, "WallpaperStyle")
        winreg.CloseKey(key)
        return True
    except:
        traceback.print_exc()
        return False

@staticmethod
def IsProcess(name: str):
    name=os.path.basename(name)
    for p in psutil.process_iter(['name']):
        if p.info['name'].lower() == name.lower():
            return True
    return False
@staticmethod
def IsService(name: str):
    try: _=psutil.win_service_get(name)
    except: return False
    return _
@staticmethod
def GetServiceBinpath(ServiceName):
    try:
        r = subprocess.run(["sc", "qc", ServiceName], capture_output=True, text=True, check=True)
        for line in r.stdout.splitlines():
            if "BINARY_PATH_NAME" in line: return line.split(":", 1)[1].strip()
        return None
    except subprocess.CalledProcessError:
        return None

#class Command:
#    def __init__(self, cmd):
#        self.cmd = cmd
#        #startupinfo = None
#        #if sys.platform.startswith('win'):
#        startupinfo = subprocess.STARTUPINFO()
#        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
#        startupinfo.wShowWindow = subprocess.SW_HIDE
#        #else:
#        #    creationflags = 0
#        self.result = subprocess.run(
#            cmd,
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#            universal_newlines=True,
#            shell=False,
#            startupinfo=startupinfo,
#            creationflags=subprocess.CREATE_NO_WINDOW
#        )
#        self.stdout = self.result.stdout
#        self.stderr = self.result.stderr
#        self.returncode = self.result.returncode
#    def __str__(self):
#        return self.stdout
#    def count(self, substring):
#        return self.stdout.count(substring) + self.stderr.count(substring)
#    def ishad(self, items):
#        if not isinstance(items, (list, tuple, set)): items = [items]
#        return any(self.count(item) > 0 for item in items)
#    def successtatus(self):
#        return self.ishad(["success", "successfully", "成功"])

class Command:
    def __init__(self, cmd):
        self.cmd = " ".join(cmd) if type(cmd) == list else cmd
        self.result = os.popen(self.cmd).read()
        self.returncode = self.result
    def __str__(self):
        return self.result
    def count(self, substring):
        return self.result.count(substring)
    def ishad(self, items):
        if not isinstance(items, (list, tuple, set)): items = [items]
        return any(self.count(item) > 0 for item in items)
    def successtatus(self):
        return self.ishad(["success", "successfully", "成功"])

class WindowsService:
    @staticmethod
    def StartService(ServiceName):
        try:
            win32serviceutil.StartService(ServiceName)
            return True
        except pywintypes.error as e: return e.winerror
    @staticmethod
    def StopService(ServiceName):
        try:
            win32serviceutil.StopService(ServiceName)
            return True
        except pywintypes.error as e: return e.winerror


def DisableNetwork():
    system = platform.system()
    if system == "Linux":
        result = subprocess.run(['ip', '-o', 'link', 'show'], capture_output=True, text=True)
        interfaces = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'state UP' in line]
        if interfaces:
            for interface in interfaces:
                subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'])
            return interfaces
    elif system == "Windows":
        result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        connections = [line.split('  ')[-1].strip() for line in result.stdout.split('\n') 
                      if 'Connected' in line and not 'Loopback' in line]
        if connections:
            for conn in connections:
                subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{conn}"', 'admin=disable'])
            return connections
    return None
def EnableNetwork(interfaces):
    system = platform.system()
    if system == "Linux" and interfaces:
        for interface in interfaces:
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'])
    elif system == "Windows" and interfaces:
        for conn in interfaces:
            subprocess.run(['netsh', 'interface', 'set', 'interface', f'name="{conn}"', 'admin=enable'])



class WindowsScreenCapture:
    """Windows platform screen capture utility"""
    def __init__(self):
        # Configure console encoding for Chinese display
        # Initialize Windows API
        self.user32 = ctypes.windll.user32
        self.gdi32 = ctypes.windll.gdi32
        # Define necessary structures
        class CURSORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("flags", ctypes.c_uint),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.wintypes.POINT)
            ]
        class ICONINFO(ctypes.Structure):
            _fields_ = [
                ("fIcon", ctypes.c_bool),
                ("xHotspot", ctypes.c_uint),
                ("yHotspot", ctypes.c_uint),
                ("hbmMask", ctypes.c_void_p),
                ("hbmColor", ctypes.c_void_p)
            ]
        self.CURSORINFO = CURSORINFO
        self.ICONINFO = ICONINFO
    @property
    def X(self):
        return win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    @property
    def Y(self):
        return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    def GetCursorPosition(self):
        """Get current mouse cursor position"""
        cursor_info = self.CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(cursor_info)
        self.user32.GetCursorInfo(ctypes.byref(cursor_info))
        return cursor_info.ptScreenPos.x, cursor_info.ptScreenPos.y
    def GetCursorImage(self):
        """Get mouse cursor image"""
        cursor_info = self.CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(cursor_info)
        self.user32.GetCursorInfo(ctypes.byref(cursor_info))
        if cursor_info.flags != 1:  # CURSOR_SHOWING
            return None, (0, 0)
        icon_info = self.ICONINFO()
        self.user32.GetIconInfo(cursor_info.hCursor, ctypes.byref(icon_info))
        # Get cursor dimensions
        cursor_width = self.user32.GetSystemMetrics(0)  # SM_CXCURSOR
        cursor_height = self.user32.GetSystemMetrics(1)  # SM_CYCURSOR
        # Create cursor image
        cursor_bmp = Image.new("RGBA", (cursor_width, cursor_height), (0, 0, 0, 0))
        return cursor_bmp, (icon_info.xHotspot, icon_info.yHotspot)
    def CaptureScreenWithCursor(self):
        """Capture screen with mouse cursor"""
        # Capture screen
        screenshot = ImageGrab.grab()
        # Get cursor position and image
        cursor_pos = self.GetCursorPosition()
        cursor_image, hotspot = self.GetCursorImage()
        if cursor_image:
            # Calculate position to draw cursor
            draw_x = cursor_pos[0] - hotspot[0]
            draw_y = cursor_pos[1] - hotspot[1]
            # Paste cursor onto screenshot
            screenshot.paste(cursor_image, (draw_x, draw_y), cursor_image)
        return screenshot
    def CompressImageWithLevel(self, image, compression_level=10):
        """
        Compress image based on compression level (0-20)
        Level 0: Original image (saved as PNG)
        Level 1-20: Increasing compression with higher levels
        """
        # Validate compression level
        compression_level = max(0, min(20, compression_level))
        # Level 0 returns original image as PNG
        if compression_level == 0:
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            return buffer.getvalue(), "png"
        # Calculate compression parameters based on level
        quality = 95 - (compression_level * 4.5)  # Quality from 95 (level 1) to 10 (level 20)
        size_factor = 1.0 - ((compression_level - 1) * 0.045)  # Size reduction factor
        # Resize image based on compression level
        if compression_level > 1:
            width, height = image.size
            new_width = int(width * size_factor)
            new_height = int(height * size_factor)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Convert to RGB (JPEG doesn't support RGBA)
        image = image.convert("RGB")
        # Save with calculated quality
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=int(quality), optimize=True)
        buffer.seek(0)
        data = buffer.read()
        return data, "jpg"
    def CaptureAndCompressScreenshot(self, compression_level=10, left_x=None, left_y=None, right_x=None, right_y=None):
        try:
            start_time = time.time()
            if None in (left_x, left_y, right_x, right_y):
                bbox = None
            else:
                bbox = (left_x, left_y, right_x, right_y)
            screenshot_event = threading.Event()
            cursor_event = threading.Event()
            screenshot_result = []
            cursor_result = []
            def capture_screenshot():
                try:
                    screenshot = ImageGrab.grab(bbox=bbox) if bbox else ImageGrab.grab()
                    screenshot_result.append(screenshot)
                    screenshot_event.set()
                except:
                    return False
            def capture_cursor():
                try:
                    cursor_pos = self.GetCursorPosition()
                    cursor_image, hotspot = self.GetCursorImage()
                    cursor_result.extend([cursor_pos, cursor_image, hotspot])
                    cursor_event.set()
                except:
                    return False
            t1 = threading.Thread(target=capture_screenshot)
            t2 = threading.Thread(target=capture_cursor)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            screenshot = screenshot_result[0]
            cursor_pos, cursor_image, hotspot = cursor_result
            if cursor_image:
                draw_x = cursor_pos[0] - hotspot[0]
                draw_y = cursor_pos[1] - hotspot[1]
                if bbox:
                    if (bbox[0] <= draw_x <= bbox[2] and 
                        bbox[1] <= draw_y <= bbox[3]):
                        screenshot.paste(cursor_image, (draw_x - bbox[0], draw_y - bbox[1]), cursor_image)
                else: screenshot.paste(cursor_image, (draw_x, draw_y), cursor_image)
            image_data, format = self.CompressImageWithLevel(screenshot, compression_level)
            return {
                'ImageBytes': image_data,
                'Format': format,
                'CompressionLevel': compression_level,
                'TimeElapsed': time.time() - start_time,
                'FileSize': len(image_data),
                'IsRegion': bbox is not None,
                'Region': bbox if bbox else None
            }
        except Exception as e:
            return None
    def AdjustCoordinatesAdvanced(self, K, min_coord, max_coord, delta_x=25, delta_y=25):
        x, y = K
        min_x, min_y = min_coord
        max_x, max_y = max_coord
        decreased = (
            max(x - delta_x, min_x),
            max(y - delta_y, min_y)
        )
        increased = (
            min(x + delta_x, max_x),
            min(y + delta_y, max_y)
        )
        return decreased, increased

def ReadFileRangeFromEnd(FilePath, StartLineFromEnd, EndLineFromEnd, BufferSize=1024 * 10, ReturnType=str):
    if StartLineFromEnd < 1 or EndLineFromEnd < 1:
        raise ValueError("Line number must be greater than 0")
    if StartLineFromEnd > EndLineFromEnd:
        raise ValueError("StartLineFromEnd must be less than or equal to EndLineFromEnd")
    LineCount = EndLineFromEnd
    BufferSize = BufferSize * LineCount
    with open(FilePath, 'rb') as FileObj:
        FileObj.seek(0, 2)
        FileSize = FileObj.tell()
        BufferSize = min(BufferSize, FileSize)
        Lines = []
        CurrentPosition = FileSize
        FoundLines = 0
        while CurrentPosition > 0 and FoundLines < LineCount:
            ReadPosition = max(0, CurrentPosition - BufferSize)
            ChunkSize = CurrentPosition - ReadPosition
            FileObj.seek(ReadPosition)
            Chunk = FileObj.read(ChunkSize)
            ChunkLines = Chunk.splitlines()
            ChunkLines = ChunkLines[::-1]
            for Line in ChunkLines:
                if FoundLines < LineCount:
                    Lines.append(Line)
                    FoundLines += 1
                else:
                    break
            CurrentPosition = ReadPosition
        Lines = Lines[::-1]
        StartIndex = max(0, len(Lines) - EndLineFromEnd)
        EndIndex = len(Lines) - StartLineFromEnd + 1
        ResultLines = Lines[StartIndex:EndIndex]
        R = [Line.decode('utf-8', errors='ignore') for Line in ResultLines]
        if ReturnType == str: return '\n'.join(R)
        elif ReturnType == list: return R
        else: raise ValueError("Return Type Error")

def GetFileSha256(FilePath: str, ChunkSize=4096) -> str:
    Sha256Hash = hashlib.sha256()
    with open(FilePath, 'rb') as f:
        while True:
            chunk = f.read(ChunkSize)
            if not chunk: break
            Sha256Hash.update(chunk)
    return Sha256Hash.hexdigest()

def GetBytesSha256(Data: bytes, ChunkSize=4096) -> str:
    Sha256Hash = hashlib.sha256()
    for i in range(0, len(Data), ChunkSize):
        Sha256Hash.update(Data[i:i+ChunkSize])
    return Sha256Hash.hexdigest()

def IsSha256(s):
    return bool(re.fullmatch(r'[a-fA-F0-9]{64}', s))


class FileSystemPermissionEnforcer:
    @staticmethod
    def _setFilePermissionsWithTakeOwnership(hFile, sid=None):
        try:
            if sid is None: sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.GetFileSecurity(hFile, win32security.OWNER_SECURITY_INFORMATION)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithBackupRestore(hFile):
        try:
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
            )
            win32security.AdjustTokenPrivileges(
                token,
                False,
                [
                    (win32security.LookupPrivilegeValue(None, win32security.SE_BACKUP_NAME), win32security.SE_PRIVILEGE_ENABLED),
                    (win32security.LookupPrivilegeValue(None, win32security.SE_RESTORE_NAME), win32security.SE_PRIVILEGE_ENABLED),
                ]
            )
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION | win32security.OWNER_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithTakeOwnershipPrivilege(hFile):
        try:
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
            )
            win32security.AdjustTokenPrivileges(
                token,
                False,
                [
                    (win32security.LookupPrivilegeValue(None, win32security.SE_TAKE_OWNERSHIP_NAME), win32security.SE_PRIVILEGE_ENABLED),
                ]
            )
            return FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnership(hFile)
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithAdminPrivilege(hFile):
        try:
            adminSid = win32security.LookupAccountName("", "Administrators")[0]
            secDesc = win32security.GetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION)
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                adminSid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(hFile, win32security.DACL_SECURITY_INFORMATION, secDesc)
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithForceMode(hFile):
        try:
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(
                hFile,
                win32security.DACL_SECURITY_INFORMATION | 
                win32security.OWNER_SECURITY_INFORMATION | 
                win32security.GROUP_SECURITY_INFORMATION,
                secDesc
            )
            return True
        except Exception: return False
    @staticmethod
    def _setFilePermissionsWithInheritance(hFile):
        try:
            sid = win32security.LookupAccountName("", win32api.GetUserName())[0]
            secDesc = win32security.SECURITY_DESCRIPTOR()
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.GENERIC_ALL,
                sid
            )
            secDesc.SetSecurityDescriptorDacl(1, dacl, 0)
            secDesc.SetSecurityDescriptorOwner(sid, False)
            win32security.SetFileSecurity(
                hFile,
                win32security.DACL_SECURITY_INFORMATION | 
                win32security.OWNER_SECURITY_INFORMATION | 
                win32security.PROTECTED_DACL_SECURITY_INFORMATION,
                secDesc
            )
            return True
        except Exception: return False
    @staticmethod
    def _tryAllPermissionMethods(filePath):
        methods = [
            FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnership,
            FileSystemPermissionEnforcer._setFilePermissionsWithBackupRestore,
            FileSystemPermissionEnforcer._setFilePermissionsWithTakeOwnershipPrivilege,
            FileSystemPermissionEnforcer._setFilePermissionsWithAdminPrivilege,
            FileSystemPermissionEnforcer._setFilePermissionsWithForceMode,
            FileSystemPermissionEnforcer._setFilePermissionsWithInheritance,
        ]
        try:
            hFile = win32file.CreateFile(
                filePath,
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
            for method in methods:
                try: return method(hFile)
                except Exception: continue
            return False
        finally:
            try:
                if 'hFile' in locals(): win32file.CloseHandle(hFile)
            except: pass
    @staticmethod
    def enforcePermissionsRecursive(folderPath):
        try:
            if not FileSystemPermissionEnforcer._tryAllPermissionMethods(folderPath):
                return False
            for root, dirs, files in os.walk(folderPath):
                for dirName in dirs:
                    dirPath = os.path.join(root, dirName)
                    if not FileSystemPermissionEnforcer._tryAllPermissionMethods(dirPath):
                        return False
                for fileName in files:
                    filePath = os.path.join(root, fileName)
                    if not FileSystemPermissionEnforcer._tryAllPermissionMethods(filePath):
                        return False
            return True
        except Exception:
            return False

def GetPidsPath(Path):
    pids = []
    for proc in psutil.process_iter(['pid', 'exe']):
        try:
            if proc.info['exe'] and proc.info['exe'].lower() == Path.lower():
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
    return pids