from PyQt5.QtWidgets import QFileDialog


def show_file(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getOpenFileName(self, "Load Settings File", "", "INI Files (*.ini);;All Files (*)",
                                              options=options)
    return filename
