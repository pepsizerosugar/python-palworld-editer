"""Entrypoint for launching the Palworld settings editor GUI."""

import sys

import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.dataclass.ui_elements import UIElements
from gui.initialize import InitializeUI


class MainClass(QMainWindow):
    """Top-level window that hosts the browse UI."""

    def __init__(self) -> None:
        """Assign the browse window and initialize UI elements."""

        super().__init__()
        UIElements.browse_window = self
        InitializeUI.__init__(self)


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/img/icon.ico"))
    qtmodern.styles.dark(app)

    window = MainClass()
    modern_window = qtmodern.windows.ModernWindow(window)
    modern_window.show()

    sys.exit(app.exec_())
