from sys import exit
from multiprocessing import freeze_support
import gui.main

if __name__ == "__main__":
    freeze_support()
    gui.main.MainWindow.show()
    exit(gui.main.App.exec())