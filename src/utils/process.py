from multiprocessing import Process
from multiprocessing import Pipe
from traceback import format_exc
from subprocess import check_output, CREATE_NO_WINDOW, Popen, PIPE
from os import path

class ProcessWithException(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self.pconn, self.cconn = Pipe()
        self.exc, self.tb = None, None

    def run(self):
        try:
            Process.run(self)
            self._cconn.send((None,None))
        except Exception as exc:
            tb = format_exc()
            self.cconn.send((exc, tb))

    def catch_exception(self):
        if self.pconn.poll():
            self.exc, self.tb = self.pconn.recv()
        return self.exc, self.tb

    def wait_for_exception(self):
        while True:
            exc = self.send_exception()
            if any(exc):
                return exc

def process_list():
    return check_output(["tasklist"],shell=False,creationflags=CREATE_NO_WINDOW).split(b"\r\n")[3:]

def start(executable):
    return Popen([path.basename(executable)],shell=True,creationflags=CREATE_NO_WINDOW,cwd=path.dirname(executable), stdout=PIPE, stderr=PIPE)

def run(cmd):
    return Popen(cmd,shell=False,creationflags=CREATE_NO_WINDOW)

def kill(process):
    return Popen(["taskkill","-f","-im",process,"-t"],shell=False,creationflags=CREATE_NO_WINDOW)
