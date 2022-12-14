from PyQt5.QtCore import Qt, QThread, pyqtSignal
from keyboard import is_pressed
from utils.process import ProcessWithException
import autoplayer.main

class Autoplayer(QThread):
    exception_signal = pyqtSignal(tuple)
    stopped_signal = pyqtSignal()

    def __init__(self,*args,**kwargs):
        return super().__init__(*args,**kwargs)


    def run(self):
        autoplayer.main.SCROLL_DELAY = self.parent().scroll_delay
        autoplayer.main.VIDEO_CHECK_DELAY = self.parent().video_check_delay

        self.autoplayer_process = ProcessWithException(target=autoplayer.main.start)
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

