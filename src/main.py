from sys import exit, argv
from multiprocessing import freeze_support
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import gui.main

if __name__ == "__main__":
    freeze_support()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    gui_app = QApplication(argv)
    main_window = gui.main.MainWindow()

    main_window.show()

    exit(gui_app.exec())
