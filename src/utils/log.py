from os import path, mkdir
from time import strftime
from .constants import File
from .process import start


class Log:
    def __init__(self,filename):
        if not path.exists(File.LOG_PATH):
            mkdir(File.LOG_PATH)

        self.filename = f"{filename} - {strftime('%d.%m.%Y %H.%M.%S')}.log"
        self.file_io = open(f"{File.LOG_PATH}\\{self.filename}","w")

    def write(self, text):
        self.file_io.write(f"[{strftime('%d.%m.%Y %H:%M:%S')}] {text}\n")
        self.file_io.flush()

    def open(self):
        start(f"{File.LOG_PATH}\\{self.filename}")

    def close(self):
        self.file_io.close()

def create_log(log_name, file_name):
    exec(f"""
global {log_name}

{log_name} = Log({repr(file_name)})
    """)

