from utils.main import main as _main
from utils.process import Process as _Process
from utils.process import process_list as _process_list
from utils.log import Log as _Log

def main():
    return _main()

class Process(_Process):
    pass

def process_list():
    return _process_list()

class Log(_Log):
    pass
