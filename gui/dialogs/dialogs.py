from PyQt5.QtWidgets import QFileDialog

from gui.dataclass.ui_elements import UIElements


def show_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getOpenFileName(UIElements.main_window, "Load Settings File", "",
                                              "INI Files (*.ini);;All Files (*)",
                                              options=options)
    return filename
