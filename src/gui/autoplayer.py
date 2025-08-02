from PyQt5.QtCore import QThread, pyqtSignal
from keyboard import is_pressed
from utils.process import ProcessWithException
import autoplayer.main

class Autoplayer(QThread):
    exception_signal = pyqtSignal(tuple)
    stopped_signal = pyqtSignal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self):
        self.autoplayer_process = ProcessWithException(target=autoplayer.main.start, args=(self.parent().scroll_delay, self.parent().video_check_delay, self.parent().page_loading_delay))
        self.autoplayer_process.start()

        while True:
            exception = self.autoplayer_process.catch_exception()

            if is_pressed(self.parent().shortcut):
                self.autoplayer_process.terminate()
                self.stopped_signal.emit()
                break

            if all(exception):
                self.autoplayer_process.terminate()
                self.exception_signal.emit(exception)
                break

