from sys import exit, argv
from multiprocessing import freeze_support
from PyQt5.QtWidgets import QApplication
import gui.main

if __name__ == "__main__":
    freeze_support()

    gui_app = QApplication(argv)
    main_window = gui.main.MainWindow()

    main_window.show()

    exit(gui_app.exec())