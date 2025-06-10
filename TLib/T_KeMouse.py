from .T_imports import *
from .T_CDLL import *



'''
class KeMouse:
    def __init__(self, cdll):
        self.lib = cdll
        self.__init__set__()
    def __init__set__(self):
        try:
            # 设置DLL函数原型
            self.lib.CaptureScreenGray.restype = ctypes.POINTER(GrayImage)
            self.lib.CaptureScreenGray.argtypes = []
            
            self.lib.LoadImageGray.restype = ctypes.POINTER(GrayImage)
            self.lib.LoadImageGray.argtypes = [ctypes.c_char_p]
            
            self.lib.FindTemplateOptimized.restype = Point
            self.lib.FindTemplateOptimized.argtypes = [
                ctypes.POINTER(GrayImage), 
                ctypes.POINTER(GrayImage), 
                ctypes.c_double  # 明确指定为double类型
            ]
            
            self.lib.FreeGrayImage.restype = None
            self.lib.FreeGrayImage.argtypes = [ctypes.POINTER(GrayImage)]
            
            # 初始化鼠标控制
            self.user32 = ctypes.WinDLL('user32', use_last_error=True)
            self.user32.SendInput.argtypes = (ctypes.c_uint, ctypes.POINTER(Input), ctypes.c_int)
            self.user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
            
        except Exception as e:
            raise RuntimeError(f"初始化失败: {str(e)}")

    def FindTargetPng(self, target_png: str, threshold: float = 0.9, screen_scale: float = 1) -> typing.Optional[typing.Tuple[int, int]]:
        try:
            # 加载目标图像
            target = self.lib.LoadImageGray(target_png.encode('utf-8'))
            if not target:
                raise ValueError("无法加载目标图像")
                
            # 捕获屏幕并查找目标
            screen = self.lib.CaptureScreenGray()
            pos = self.lib.FindTemplateOptimized(screen, target, ctypes.c_double(threshold))
            
            # 应用屏幕缩放
            if screen_scale != 1:
                pos.x = int(pos.x * screen_scale)
                pos.y = int(pos.y * screen_scale)
            
            # 释放资源
            self.lib.FreeGrayImage(target)
            self.lib.FreeGrayImage(screen)
            
            return (pos.x, pos.y) if pos.x != -1 else None
            
        except Exception as e:
            raise RuntimeError(f"查找目标失败: {str(e)}")

    def ClickAt(self, x: int, y: int, button: str = 'left'):
        """在指定坐标执行鼠标点击"""
        self.user32.SetCursorPos(x, y)
        
        # 准备输入事件
        inputs = (Input * 2)()
        button = button.lower()
        
        # 设置鼠标事件标志
        down_flag, up_flag = {
            'left': (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
            'right': (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
            'middle': (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP)
        }.get(button, (None, None))
        
        if down_flag is None:
            raise ValueError(f"不支持的鼠标按钮: {button}")
        
        # 鼠标按下和释放事件
        inputs[0].type = INPUT_MOUSE
        inputs[0].union.mi.dwFlags = down_flag
        inputs[1].type = INPUT_MOUSE
        inputs[1].union.mi.dwFlags = up_flag
        
        # 发送输入事件
        self.user32.SendInput(2, inputs, ctypes.sizeof(Input))

    def ClickTargetPNG(self, target: str, threshold: float = 0.9, 
                      button: str = 'left', ScreenScale: float = 1, 
                      sleep: float = 0) -> bool:
        """查找目标并点击"""
        try:
            pos = self.FindTargetPng(target, threshold, ScreenScale)
            if not pos:
                return False
                
            self.ClickAt(pos[0], pos[1], button)
            if sleep > 0:
                time.sleep(sleep)
            return True
            
        except Exception as e:
            raise RuntimeError(f"点击目标失败: {str(e)}")
'''


class KeMouse:
    def __init__(self, cdll):
        self.lib=cdll

        # 设置函数原型
        self.lib.CaptureScreenGray.restype = ctypes.POINTER(GrayImage)
        self.lib.CaptureScreenGray.argtypes = [ctypes.POINTER(ctypes.c_int)]
        
        self.lib.LoadImageGray.restype = ctypes.POINTER(GrayImage)
        self.lib.LoadImageGray.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        
        self.lib.FindTemplateOptimized.restype = MatchResult
        self.lib.FindTemplateOptimized.argtypes = [
            ctypes.POINTER(GrayImage), 
            ctypes.POINTER(GrayImage), 
            ctypes.c_double,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]
        
        self.lib.FreeGrayImage.restype = None
        self.lib.FreeGrayImage.argtypes = [ctypes.POINTER(GrayImage)]
        
        self.lib.ClickAt.restype = ctypes.c_int
        self.lib.ClickAt.argtypes = [ctypes.c_int, ctypes.c_int]
        
        self.lib.Initialize.restype = ctypes.c_int
        self.lib.Initialize.argtypes = []
        
        # 初始化
        if self.lib.Initialize() != 0:
            raise RuntimeError("初始化失败")

        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        
        # 设置函数原型
        self.user32.SendInput.restype = ctypes.wintypes.UINT
        self.user32.SendInput.argtypes = (
            ctypes.wintypes.UINT,      # nInputs
            ctypes.POINTER(Input),  # pInputs
            ctypes.c_int        # cbSize
        )
        
        self.user32.SetCursorPos.restype = ctypes.wintypes.BOOL
        self.user32.SetCursorPos.argtypes = (
            ctypes.wintypes.INT,      # X
            ctypes.wintypes.INT       # Y
        )
        
        self.user32.GetCursorPos.restype = ctypes.wintypes.BOOL
        self.user32.GetCursorPos.argtypes = (
            ctypes.POINTER(ctypes.wintypes.POINT),  # lpPoint
        )

    def capture_screen(self) -> typing.Optional[GrayImage]:
        error_code = ctypes.c_int(0)
        screen = self.lib.CaptureScreenGray(ctypes.byref(error_code))
        if error_code.value != 0 or not screen:
            raise RuntimeError(f"屏幕捕获失败，错误码: {error_code.value}")
        return screen

    def load_image(self, filename: str) -> typing.Optional[GrayImage]:
        error_code = ctypes.c_int(0)
        try:
            encoded = filename.encode('utf-8')
            target = self.lib.LoadImageGray(encoded, ctypes.byref(error_code))
            if error_code.value != 0:
                raise RuntimeError(f"图像加载失败，错误码: {error_code.value}")
            if not target:
                raise RuntimeError("返回了空指针")
            return target
        except Exception as e:
            raise RuntimeError(f"加载图像时出错: {str(e)}")

    def find_template(self, target: str, threshold: float = 0.9, search_area: typing.Optional[typing.Tuple[int, int, int, int]] = None) -> typing.Tuple[typing.Optional[typing.Tuple[int, int]], float]:
        #try:
            target=os.path.abspath(target)
            if not os.path.isfile(target):
                raise FileNotFoundError(target)
            target_img = self.load_image(target)
            screen = self.capture_screen()
            x1, y1, x2, y2 = -1, -1, -1, -1
            if search_area is not None:
                x1, y1, x2, y2 = search_area
            result = self.lib.FindTemplateOptimized(screen, target_img, threshold, x1, y1, x2, y2)
            self.lib.FreeGrayImage(target_img)
            self.lib.FreeGrayImage(screen)
            if result.error != 0:
                if result.error == 202:
                    return None, result.confidence
                raise RuntimeError(f"ErrorCode: {result.error}")
            return (result.x, result.y), result.confidence
        #except Exception as e:
        #    raise RuntimeError(f"查找目标失败: {str(e)}")

    def move_to(self, x, y):
        """移动鼠标到指定位置"""
        if not self.user32.SetCursorPos(x, y):
            raise ctypes.WinError(ctypes.get_last_error())

    def get_position(self):
        """获取当前鼠标位置"""
        point = ctypes.wintypes.POINT()
        if not self.user32.GetCursorPos(ctypes.byref(point)):
            raise ctypes.WinError(ctypes.get_last_error())
        return (point.x, point.y)

    def click(self, x=None, y=None, button='left', double=False, delay=0.1) -> bool:
        """
        模拟鼠标点击并返回是否成功
        :param x: X坐标 (None表示当前位置)
        :param y: Y坐标 (None表示当前位置)
        :param button: 'left' 或 'right'
        :param double: 是否双击
        :param delay: 两次点击之间的延迟(秒)
        :return: True表示成功，False表示失败
        """
        try:
            # 移动鼠标到指定位置
            if x is not None and y is not None:
                if not self.user32.SetCursorPos(x, y):
                    return False

            # 获取当前鼠标位置
            point = ctypes.wintypes.POINT()
            if not self.user32.GetCursorPos(ctypes.byref(point)):
                return False
            x, y = point.x, point.y

            # 设置鼠标事件标志
            button = button.lower()
            down_flag, up_flag = {
                'left': (0x0002, 0x0004),  # MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
                'right': (0x0008, 0x0010), # MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
                'middle': (0x0020, 0x0040) # MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
            }.get(button, (None, None))

            if down_flag is None:
                return False

            # 创建输入事件
            def create_input(dwFlags):
                inp = Input()
                inp.type = 0  # INPUT_MOUSE
                inp.union.mi.dwFlags = dwFlags
                inp.union.mi.dx = x
                inp.union.mi.dy = y
                return inp

            # 准备输入事件数组
            inputs = []
            inputs.append(create_input(down_flag))
            inputs.append(create_input(up_flag))
            
            if double:
                time.sleep(delay)
                inputs.append(create_input(down_flag))
                inputs.append(create_input(up_flag))

            # 转换为C数组
            input_array = (Input * len(inputs))(*inputs)
            
            # 发送输入并检查结果
            sent = self.user32.SendInput(
                len(inputs),
                input_array,
                ctypes.sizeof(Input)
            )
            
            return sent == len(inputs)
            
        except Exception:
            return False

    def ClickTargetPNG(self, target: str, button: str='left', threshold: float = 0.9, sleep: float = 0, search_area: typing.Optional[typing.Tuple[int, int, int, int]] = None) -> bool:
        pos, confidence = self.find_template(target, threshold, search_area)
        if not pos:
            return False
        _=self.click(pos[0], pos[1], button=button)
        time.sleep(sleep)
        return _

    def ClickTargetPNGAC(self, target: str, button: str='left', threshold: float = 0.9, sleep: float = 0, search_area: typing.Optional[typing.Tuple[int, int, int, int]] = None, confidence = 0.9) -> bool:
        _pos, _confidence = self.find_template(target, threshold, search_area)
        if not _pos or _confidence < confidence:
            return False
        _=self.click(_pos[0], _pos[1], button=button)
        time.sleep(sleep)
        return _
    def ScreenshotBytes(self):
        hdesktop = win32gui.GetDesktopWindow()
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        hdc = win32gui.GetWindowDC(hdesktop)
        mfc_dc = win32ui.CreateDCFromHandle(hdc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(bitmap)
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        pil_img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr,
            'raw',
            'BGRX',
            0, 1
        )
        img_bytes = io.BytesIO()
        pil_img.save(img_bytes, format='PNG')
        p = img_bytes.getvalue()
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hdc)
        return p