from .T_imports import *


def GetWindowsSystemINFO():
    info = {}  # 创建一个空字典，用于存储所有系统信息

    # 使用 sys 模块收集信息
    info['sys'] = {
        'platform': sys.platform,  # 操作系统平台（如 'win32'）
        'version': sys.version,  # Python 解释器版本
        'executable': sys.executable,  # Python 解释器路径
        'argv': sys.argv,  # 命令行参数
        'path': sys.path,  # Python 模块搜索路径
        'maxsize': sys.maxsize,  # 最大整数值
        'maxunicode': sys.maxunicode,  # 最大 Unicode 值
        'copyright': sys.copyright,  # Python 版权信息
        'hexversion': sys.hexversion,  # Python 版本的十六进制表示
    }

    # 使用 os 模块收集信息
    info['os'] = {
        'name': os.name,  # 操作系统名称（如 'nt'）
        'environ': dict(os.environ),  # 环境变量
        'login': os.getlogin(),  # 当前登录用户
        'envlogin': os.getenv('USERNAME'),  # 环境变量中的用户名
        'cwd': os.getcwd(),  # 当前工作目录
        'cpu_count': os.cpu_count(),  # CPU 核心数
        'pid': os.getpid(),  # 当前进程 ID
        'ppid': os.getppid(),  # 父进程 ID
        'sep': os.sep,  # 路径分隔符
        'pathsep': os.pathsep,  # 路径列表分隔符
        'linesep': os.linesep,  # 行分隔符
        'devices': os.listdir(os.getenv("SystemDrive")+"\\"),  # C 盘根目录下的文件和文件夹
    }

    # 使用 platform 模块收集信息
    info['platform'] = {
        'system': platform.system(),  # 操作系统名称（如 'Windows'）
        'node': platform.node(),  # 网络名称（主机名）
        'release': platform.release(),  # 操作系统版本
        'version': platform.version(),  # 操作系统详细信息
        'machine': platform.machine(),  # 机器类型（如 'AMD64'）
        'processor': platform.processor(),  # 处理器信息
        'win32_ver': platform.win32_ver(),  # Windows 版本信息
        'python_build': platform.python_build(),  # Python 构建信息
        'python_compiler': platform.python_compiler(),  # Python 编译器信息
        'python_branch': platform.python_branch(),  # Python 分支信息
        'python_implementation': platform.python_implementation(),  # Python 实现（如 'CPython'）
        'python_revision': platform.python_revision(),  # Python 修订版本号
        'python_version': platform.python_version(),  # Python 版本号
        'python_version_tuple': platform.python_version_tuple(),  # Python 版本号元组
    }

    # 使用 ctypes 模块调用 Windows API 收集信息
    kernel32 = ctypes.windll.kernel32
    advapi32 = ctypes.windll.advapi32
    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32
    gdi32 = ctypes.windll.gdi32
    iphlpapi = ctypes.windll.iphlpapi
    version = ctypes.windll.version
    userenv = ctypes.windll.userenv

    # 定义 SYSTEM_INFO 结构体
    class SYSTEM_INFO(ctypes.Structure):
        _fields_ = [
            ("wProcessorArchitecture", ctypes.c_ushort),
            ("wReserved", ctypes.c_ushort),
            ("dwPageSize", ctypes.c_ulong),
            ("lpMinimumApplicationAddress", ctypes.c_void_p),
            ("lpMaximumApplicationAddress", ctypes.c_void_p),
            ("dwActiveProcessorMask", ctypes.c_ulong),
            ("dwNumberOfProcessors", ctypes.c_ulong),
            ("dwProcessorType", ctypes.c_ulong),
            ("dwAllocationGranularity", ctypes.c_ulong),
            ("wProcessorLevel", ctypes.c_ushort),
            ("wProcessorRevision", ctypes.c_ushort),
        ]

    # 获取系统信息
    system_info = SYSTEM_INFO()
    kernel32.GetSystemInfo(ctypes.byref(system_info))

    # 获取计算机名称
    computer_name = ctypes.create_string_buffer(1024)
    computer_name_size = ctypes.c_int(1024)
    kernel32.GetComputerNameA(computer_name, ctypes.byref(computer_name_size))

    # 获取用户名
    user_name = ctypes.create_string_buffer(1024)
    user_name_size = ctypes.c_int(1024)
    advapi32.GetUserNameA(user_name, ctypes.byref(user_name_size))

    # 获取系统目录
    system_directory = ctypes.create_string_buffer(1024)
    kernel32.GetSystemDirectoryA(system_directory, 1024)

    # 获取 Windows 目录
    windows_directory = ctypes.create_string_buffer(1024)
    kernel32.GetWindowsDirectoryA(windows_directory, 1024)

    # 获取内存状态
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))

    # 获取屏幕分辨率
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    color_active_caption = user32.GetSysColor(2)  # 活动窗口标题栏颜色

    # 获取特殊文件夹路径
    desktop_path = ctypes.create_unicode_buffer(1024)
    shell32.SHGetFolderPathW(0, 0x0000, None, 0, desktop_path)  # 桌面路径

    # 获取网络适配器信息
    class MIB_IFROW(ctypes.Structure):
        _fields_ = [
            ("wszName", ctypes.c_wchar * 256),
            ("dwIndex", ctypes.c_ulong),
            ("dwType", ctypes.c_ulong),
            ("dwMtu", ctypes.c_ulong),
            ("dwSpeed", ctypes.c_ulong),
            ("dwPhysAddrLen", ctypes.c_ulong),
            ("bPhysAddr", ctypes.c_ubyte * 8),
            ("dwAdminStatus", ctypes.c_ulong),
            ("dwOperStatus", ctypes.c_ulong),
            ("dwLastChange", ctypes.c_ulong),
            ("dwInOctets", ctypes.c_ulong),
            ("dwInUcastPkts", ctypes.c_ulong),
            ("dwInNUcastPkts", ctypes.c_ulong),
            ("dwInDiscards", ctypes.c_ulong),
            ("dwInErrors", ctypes.c_ulong),
            ("dwInUnknownProtos", ctypes.c_ulong),
            ("dwOutOctets", ctypes.c_ulong),
            ("dwOutUcastPkts", ctypes.c_ulong),
            ("dwOutNUcastPkts", ctypes.c_ulong),
            ("dwOutDiscards", ctypes.c_ulong),
            ("dwOutErrors", ctypes.c_ulong),
            ("dwOutQLen", ctypes.c_ulong),
            ("dwDescrLen", ctypes.c_ulong),
            ("bDescr", ctypes.c_ubyte * 256),
        ]

    if_row = MIB_IFROW()
    if_row.dwIndex = 1  # 第一个网络适配器
    iphlpapi.GetIfEntry(ctypes.byref(if_row))

    # 获取文件版本信息
    file_version_info_size = version.GetFileVersionInfoSizeW(sys.executable, None)
    file_version_info = ctypes.create_string_buffer(file_version_info_size)
    version.GetFileVersionInfoW(sys.executable, 0, file_version_info_size, file_version_info)

    # 获取显示设备信息（如果可用）
    try:
        class DISPLAY_DEVICE(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("DeviceName", ctypes.c_wchar * 32),
                ("DeviceString", ctypes.c_wchar * 128),
                ("StateFlags", ctypes.c_ulong),
                ("DeviceID", ctypes.c_wchar * 128),
                ("DeviceKey", ctypes.c_wchar * 128),
            ]

        display_device = DISPLAY_DEVICE()
        display_device.cb = ctypes.sizeof(DISPLAY_DEVICE)
        if hasattr(gdi32, 'EnumDisplayDevicesW'):
            gdi32.EnumDisplayDevicesW(None, 0, ctypes.byref(display_device), 0)
            display_info = {
                'DeviceName': display_device.DeviceName,
                'DeviceString': display_device.DeviceString,
                'StateFlags': display_device.StateFlags,
            }
        else:
            display_info = "EnumDisplayDevicesW not available"
    except Exception as e:
        display_info = f"Error: {str(e)}"

    # 获取用户配置文件信息
    profile_path = ctypes.create_unicode_buffer(1024)
    userenv.GetUserProfileDirectoryW(kernel32.GetCurrentProcess(), profile_path, ctypes.byref(ctypes.c_ulong(1024)))

    # 构建一个包含系统信息的字典，键为函数名或信息类别，值为对应的系统信息
    info['ctypes'] = {
        # 获取当前进程的 ID
        'GetCurrentProcessId': kernel32.GetCurrentProcessId(),  
        # 获取当前线程的 ID
        'GetCurrentThreadId': kernel32.GetCurrentThreadId(),  
        # 获取系统的基本信息
        'GetSystemInfo': {
            # 处理器架构类型
            'ProcessorArchitecture': system_info.wProcessorArchitecture,
            # 系统的页面大小
            'PageSize': system_info.dwPageSize,
            # 系统中处理器的数量
            'NumberOfProcessors': system_info.dwNumberOfProcessors,
            # 处理器的类型
            'ProcessorType': system_info.dwProcessorType,
            # 处理器的级别
            'ProcessorLevel': system_info.wProcessorLevel,
            # 处理器的修订版本号
            'ProcessorRevision': system_info.wProcessorRevision,
        },
        # 获取 Windows 操作系统的版本信息
        'GetVersion': kernel32.GetVersion(),  
        # 获取系统自启动以来经过的毫秒数（32 位）
        'GetTickCount': kernel32.GetTickCount(),  
        # 获取系统自启动以来经过的毫秒数（64 位）
        'GetTickCount64': kernel32.GetTickCount64(),  
        # 获取计算机的名称，并将字节类型转换为 UTF-8 编码的字符串
        'GetComputerName': computer_name.value.decode('utf-8'),  
        # 获取当前登录用户的用户名，并将字节类型转换为 UTF-8 编码的字符串
        'GetUserName': user_name.value.decode('utf-8'),  
        # 获取系统目录的路径，并将字节类型转换为 UTF-8 编码的字符串
        'GetSystemDirectory': system_directory.value.decode('utf-8'),  
        # 获取 Windows 目录的路径，并将字节类型转换为 UTF-8 编码的字符串
        'GetWindowsDirectory': windows_directory.value.decode('utf-8'),  
        # 获取系统的内存状态信息
        'GlobalMemoryStatusEx': {
            # 系统当前的内存使用率（百分比）
            'MemoryLoad': memory_status.dwMemoryLoad,
            # 系统的总物理内存量（字节）
            'TotalPhys': memory_status.ullTotalPhys,
            # 系统当前可用的物理内存量（字节）
            'AvailPhys': memory_status.ullAvailPhys,
            # 系统的总页面文件大小（字节）
            'TotalPageFile': memory_status.ullTotalPageFile,
            # 系统当前可用的页面文件大小（字节）
            'AvailPageFile': memory_status.ullAvailPageFile,
            # 系统的总虚拟内存大小（字节）
            'TotalVirtual': memory_status.ullTotalVirtual,
            # 系统当前可用的虚拟内存大小（字节）
            'AvailVirtual': memory_status.ullAvailVirtual,
        },
        # 获取系统的一些度量信息
        'GetSystemMetrics': {
            # 屏幕的宽度（像素）
            'ScreenWidth': screen_width,
            # 屏幕的高度（像素）
            'ScreenHeight': screen_height,
        },
        # 获取系统颜色信息
        'GetSysColor': {
            # 活动窗口标题栏的颜色
            'ActiveCaption': color_active_caption,
        },
        # 获取特定文件夹的路径
        'SHGetFolderPath': {
            # 桌面文件夹的路径
            'Desktop': desktop_path.value,
        },
        # 获取网络适配器的信息
        'GetIfEntry': {
            # 网络适配器的名称
            'AdapterName': if_row.wszName,
            # 网络适配器的索引
            'AdapterIndex': if_row.dwIndex,
            # 网络适配器的类型
            'AdapterType': if_row.dwType,
            # 网络适配器的速度
            'AdapterSpeed': if_row.dwSpeed,
            # 网络适配器的 MAC 地址，格式化为 XX:XX:XX:XX:XX:XX
            'AdapterMAC': GMAC(),
        },
        # 获取显示设备的信息
        'EnumDisplayDevices': display_info,
        # 获取当前用户的配置文件目录路径
        'GetUserProfileDirectory': {
            # 用户配置文件目录的路径
            'ProfilePath': profile_path.value,
        },
    }
    # 使用 socket 模块收集网络信息
    info['socket'] = {
        'hostname': socket.gethostname(),  # 主机名
        'ip_address': socket.gethostbyname(socket.gethostname()),  # IP 地址
        'fqdn': socket.getfqdn(),  # 完全限定域名
    }
    # 使用 psutil 模块收集系统信息
    try:
        swap_info = psutil.swap_memory()._asdict()
    except RuntimeError:
        swap_info = {'total': 0, 'used': 0, 'free': 0, 'percent': 0, 'sin': 0, 'sout': 0}
    if 'psutil' in sys.modules:
        info['psutil'] = {
            'cpu_count': psutil.cpu_count(logical=True),  # CPU 逻辑核心数
            'virtual_memory': psutil.virtual_memory()._asdict(),  # 虚拟内存信息
            'swap_memory': swap_info,  # 交换内存信息
            'disk_usage': psutil.disk_usage(os.getenv("SystemDrive"))._asdict(),  # 磁盘使用情况
            'disk_io_counters': psutil.disk_io_counters()._asdict(),  # 磁盘 I/O 统计
            'net_io_counters': psutil.net_io_counters()._asdict(),  # 网络 I/O 统计
            'boot_time': psutil.boot_time(),  # 系统启动时间
            'users': [user._asdict() for user in psutil.users()],  # 当前登录用户
        }
    info["ipinfo"]=None
    try: h=requests.get("https://ipinfo.io/json", timeout=10).json()
    except: print("ipinfo")
    else:
        if "error" not in h: info["ipinfo"]=h

    info["ipapico"]=None
    try: h=requests.get("https://ipapi.co/json", timeout=10).json()
    except: print("ipapico")
    else: info["ipapico"]=h

    info["ipapicom"]=None
    try: h=requests.get("http://ip-api.com/json/", timeout=10).json()
    except: print("ipapicomERROR")
    else: info["ipapicom"]=h
    return info

def GetPCMachineGUID():
    try:
        RegistryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        PCMachineGUID, _ = winreg.QueryValueEx(RegistryKey, "MachineGuid")
        winreg.CloseKey(RegistryKey)
        return PCMachineGUID
    except:
        return None