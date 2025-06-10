import ctypes
from ctypes import wintypes
import sys
import os

# 定义必要的Windows API结构和函数

class D2D_POINT_2F(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float)
    ]

class D2D_RECT_F(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_float),
        ('top', ctypes.c_float),
        ('right', ctypes.c_float),
        ('bottom', ctypes.c_float)
    ]

class OCR_LINE(ctypes.Structure):
    _fields_ = [
        ('content', ctypes.c_wchar_p),
        ('boundingBox', D2D_RECT_F)
    ]

class OCR_WORD(ctypes.Structure):
    _fields_ = [
        ('content', ctypes.c_wchar_p),
        ('boundingBox', D2D_RECT_F),
        ('confidence', ctypes.c_int)
    ]

# 加载必要的DLL
ole32 = ctypes.windll.ole32
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# 定义GUID结构
class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8)
    ]

    def __init__(self, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8):
        self.Data1 = l
        self.Data2 = w1
        self.Data3 = w2
        self.Data4[0] = b1
        self.Data4[1] = b2
        self.Data4[2] = b3
        self.Data4[3] = b4
        self.Data4[4] = b5
        self.Data4[5] = b6
        self.Data4[6] = b7
        self.Data4[7] = b8

# Windows OCR引擎的GUID
CLSID_OCRManager = GUID(0xCFFA3FE9, 0x3F10, 0x4A7D, 0x9D, 0x77, 0xE9, 0x5F, 0xE6, 0x1B, 0x5B, 0x1D)
IID_IOCRManager = GUID(0xE9B22836, 0x0F59, 0x4784, 0x9E, 0xEC, 0x8B, 0x6C, 0x5E, 0x9A, 0xE2, 0xE3)

# 定义COM接口
class IOCRManager(ctypes.c_void_p):
    pass

# 定义方法原型
IOCRManager._methods_ = [
    ('RecognizeImage', ctypes.c_uint32, 
     [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]),
    ('RecognizeImageFromFile', ctypes.c_uint32, 
     [ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]),
    ('RecognizeImageFromHBITMAP', ctypes.c_uint32, 
     [wintypes.HBITMAP, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]),
    ('SetLanguage', ctypes.c_uint32, [ctypes.c_wchar_p]),
    ('GetAvailableLanguages', ctypes.c_uint32, [ctypes.c_void_p, ctypes.c_void_p])
]

def recognize_image_from_file(file_path):
    # 初始化COM
    ole32.CoInitialize(None)
    
    # 创建OCR管理器实例
    ocr_manager = ctypes.POINTER(IOCRManager)()
    hr = ole32.CoCreateInstance(ctypes.byref(CLSID_OCRManager), 
                               None, 
                               1,  # CLSCTX_INPROC_SERVER
                               ctypes.byref(IID_IOCRManager), 
                               ctypes.byref(ocr_manager))
    
    if hr != 0:
        print(f"创建OCR管理器失败，错误代码: 0x{hr:X}")
        ole32.CoUninitialize()
        return None
    
    # 设置中文语言
    ocr_manager.SetLanguage("zh-CN")
    
    # 准备接收结果的变量
    line_count = wintypes.UINT()
    lines = ctypes.POINTER(OCR_LINE)()
    word_count = wintypes.UINT()
    words = ctypes.POINTER(OCR_WORD)()
    
    # 调用OCR识别
    hr = ocr_manager.RecognizeImageFromFile(file_path, 
                                          ctypes.byref(line_count), 
                                          ctypes.byref(lines), 
                                          ctypes.byref(word_count))
    
    if hr != 0:
        print(f"OCR识别失败，错误代码: 0x{hr:X}")
        ocr_manager.Release()
        ole32.CoUninitialize()
        return None
    
    # 提取识别结果
    result = []
    for i in range(line_count.value):
        line = lines[i]
        result.append(line.content)
    
    # 释放资源
    ole32.CoTaskMemFree(lines)
    ole32.CoTaskMemFree(words)
    ocr_manager.Release()
    ole32.CoUninitialize()
    
    return '\n'.join(result)

if __name__ == "__main__":
    image_path = "./1.png"
    
    if not os.path.exists(image_path):
        print(f"错误: 文件 {image_path} 不存在")
        sys.exit(1)
    
    try:
        result = recognize_image_from_file(image_path)
        if result:
            print("OCR识别结果:")
            print(result)
        else:
            print("未能识别任何文字")
    except Exception as e:
        print(f"发生错误: {e}")