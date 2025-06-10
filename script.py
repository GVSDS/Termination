import shutil
import time
import sys
import ast
import os

a=time.time()
args=r"--upx-dir=.\upx"


if "flush" in sys.argv:
    args+=" --clean"

if "nouc" not in sys.argv:
    import TLib.T_GodKeys
    import TLib.T_Version
    import TLib.T_FIO
    class A:
        __static_path__="./"
        @staticmethod
        def GetWorkMod():
            return "py"
    B=A()
    v=TLib.T_Version.Version(B)
    g=TLib.T_GodKeys.GodKeys(b"EXMODECONFIGKEYS"*2)
    j=ast.literal_eval(TLib.T_FIO.FIO.openr("./TConfig/EXEConfig.dict"))
    j["Version"]={"Termination": v.version["Version"], "Compilation": v.version["Compilation"]}
    s=b"EXMODECONFIGSTART"+g.encrypt(str(j).encode())+b"EXMODECONFIGEND"
    TLib.T_FIO.FIO.openw("./TConfig/EXEConfig.dict", str(j))
    TLib.T_FIO.FIO.openw("./TConfig/EXEConfig.bin", s, 2)

if os.path.isdir("./build"):
    shutil.rmtree("./build")

c=f"pyinstaller script.spec "+args
print(c)
os.system(c)

if "nouc" not in sys.argv:
    TLib.T_FIO.FIO.openw("./dist/Termination4.exe", 2, TLib.T_FIO.FIO.openr("./dist/Termination4.exe", 2)+b"EXMODECONFIGSTART"+s+b"EXMODECONFIGEND")

shutil.copy('./dist/Termination4.exe', './dist/Termination.bin')

print("Spend Time: ", time.time()-a)