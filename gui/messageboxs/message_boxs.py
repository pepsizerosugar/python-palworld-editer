from PyQt5.QtWidgets import QMessageBox


def if_settings_file_is_not_loaded():
    QMessageBox.warning(None, "Warning", "Settings file not loaded. Please load a settings file first.")
