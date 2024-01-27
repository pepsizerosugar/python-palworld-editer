from PyQt5.QtWidgets import QFileDialog


def dialog_for_load_settings_file(window):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getOpenFileName(window, "Load Settings File", "",
                                              "INI Files (*.ini);;All Files (*)",
                                              options=options)
    return filename


def dialog_for_save_settings_file(window):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getSaveFileName(window, "Save Settings File", "",
                                              "INI Files (*.ini);;All Files (*)",
                                              options=options)
    return filename
