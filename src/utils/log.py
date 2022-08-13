from os import environ, path, mkdir
from time import strftime
from utils.exceptions import InvalidMessageType

class Log:
    def __init__(self,name=None):
        if not all([path.exists(f"{environ['TEMP']}\\OBA_log"),path.isdir(f"{environ['TEMP']}\\OBA_log")]):
            mkdir(f"{environ['TEMP']}\\OBA_log")
        self.name = name if name else f"{strftime('%d.%m.%Y %H.%M.%S')}"

    def write(self,text,texttype):
        with open(f"{environ['TEMP']}\\OBA_log\\{self.name}.log","a") as file_io:
            if texttype.lower() == "info":
                file_io.write(f"[i] [{strftime('%d/%m/%Y %H:%M:%S')}] {text}\n")
            elif texttype.lower() == "error":
                file_io.write(f"[!!!] [{strftime('%d/%m/%Y %H:%M:%S')}] {text}\n")
            elif texttype.lower() == "warning":
                file_io.write(f"[!] [{strftime('%d/%m/%Y %H:%M:%S')}] {text}\n")
            else:
                raise InvalidMessageType(f"\"{texttype}\"")

