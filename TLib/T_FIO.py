from .T_imports import *


class IFIO:
    def openw(self, file, write, mode=1, encoding="UTF-8"):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fd = os.open(file, flags)
        try:
            if mode == 1:
                write = write.encode(encoding)
            os.write(fd, write)
        finally:
            os.close(fd)
    def opena(self, file, write, mode=1, encoding="UTF-8"):
        flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
        fd = os.open(file, flags)
        try:
            if mode == 1:
                write = write.encode(encoding)
            os.write(fd, write)
        finally:
            os.close(fd)
    def openr(self, file, mode=1, encoding="UTF-8"):
        flags = os.O_RDONLY
        fd = os.open(file, flags)
        try:
            read = os.read(fd, os.path.getsize(file))
            if mode == 1:
                read = read.decode(encoding)
        finally:
            os.close(fd)
        return read
IFIO=IFIO()

class OFIO():
    def openw(self, file, write, mode="1", encoding="UTF-8"):
        if mode == "1" or mode == 1:
            with open(file, "w", encoding=encoding) as f:
                f.write(write)
        elif mode == "2" or mode == 2:
            with open(file, "wb") as f:
                f.write(write)
    def opena(self, file, write, mode="1", encoding="UTF-8"):
        if mode == "1" or mode == 1:
            with open(file, "a", encoding=encoding) as f:
                f.write(write)
        elif mode == "2" or mode == 2:
            with open(file, "ab") as f:
                f.write(write)
    def openr(self, file, mode="1", encoding="UTF-8"):
        if mode == "1" or mode == 1:
            with open(file, "r", encoding=encoding) as f:
                read = f.read()
        elif mode == "2" or mode == 2:
            with open(file, "rb") as f:
                read = f.read()
        return read
    def HideFile(self, path):
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
FIO=OFIO()
