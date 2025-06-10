from .T_imports import *


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, option: str) -> str:
        return option
class IniConfigHandler:
    """INI Confih Handler"""
    @staticmethod
    def ReadIniToDict(file_path: str) -> typing.Dict[str, typing.Dict[str, str]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")
        config = CaseSensitiveConfigParser()
        loaded_files = config.read(file_path, encoding="utf-8")
        if not loaded_files:
            raise ValueError(f"Failed to load file: {file_path}")
        if not config.sections():
            raise ValueError("No valid sections found in the INI file.")
        return {section: dict(config.items(section)) for section in config.sections()}
    @staticmethod
    def WriteDictToIni(data: typing.Dict[str, typing.Dict[str, typing.Any]], file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")
        config = CaseSensitiveConfigParser()
        for section, items in data.items():
            config.add_section(section)
            for key, value in items.items():
                config.set(section, key, str(value))
        with open(file_path, 'w', encoding="utf-8") as f:
            config.write(f)

class Version:
    def __init__(self, master: 'Termination4.Termination'):
        self.master=master
        self.vfile=os.path.join(self.master.__static_path__, "TConfig", "version.ini")
        self._v=IniConfigHandler.ReadIniToDict(self.vfile)
        self.version=self._v
        if self.master.GetWorkMod() == "py":
            self._v["Compilation"]["Runs"]=str(int(self._v["Compilation"]["Runs"])+1)
            IniConfigHandler.WriteDictToIni(self._v, self.vfile)