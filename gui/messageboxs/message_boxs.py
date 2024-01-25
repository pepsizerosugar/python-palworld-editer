from PyQt5.QtWidgets import QMessageBox


def if_settings_file_is_not_loaded():
    QMessageBox.warning(None, "Warning", "Settings file not loaded. Please load a settings file first.")


def if_error_when_load_banner_image(e):
    QMessageBox.warning(None, "Warning", f"Error loading banner image: {e}")


def if_error_when_load_translations(e):
    QMessageBox.warning(None, "Warning", f"Error loading translations: {e}")


def if_error_when_load_settings_file(e):
    QMessageBox.warning(None, "Warning", f"Error loading settings file: {e}")


def if_error_when_save_settings_file(e):
    QMessageBox.warning(None, "Warning", f"Error saving settings file: {e}")
