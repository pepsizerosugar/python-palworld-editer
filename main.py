import sys

import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.dataclass.ui_elements import UIElements
from gui.initialize import InitializeUI
from utils.version_checker import VersionChecker


class MainClass(QMainWindow):
    def __init__(self):
        super().__init__()
        VersionChecker().check_version()
        UIElements.browse_window = self
        InitializeUI.__init__(self)


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resources/img/icon.ico'))
    qtmodern.styles.dark(app)

    window = MainClass()
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()

    sys.exit(app.exec_())
