import os
import sys

import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.dataclass.ui_elements import UIElements
from gui.initialize import InitializeUI


class MainClass(QMainWindow):
    def __init__(self):
        super().__init__()
        UIElements.main_window = self
        InitializeUI.__init__(self)


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    basedir = os.path.dirname(__file__)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, 'resources/icon.ico')))
    qtmodern.styles.dark(app)

    window = MainClass()
    # mw = qtmodern.windows.ModernWindow(window)
    window.show()

    sys.exit(app.exec_())
