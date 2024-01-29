from PyQt5.QtWidgets import QMessageBox


def if_settings_file_is_not_loaded():
    QMessageBox.warning(None, "Warning", "Settings file not loaded. Please load a settings file first.")


def if_load_settins_file_is_finished():
    QMessageBox.information(None, "Information", "Settings file loaded finished.")


def if_update_settings_finished():
    QMessageBox.information(None, "Information", "Settings updated finished.")


def if_error_when_load_metadata(e):
    QMessageBox.warning(None, "Warning", f"Error loading metadata: {e}")


def if_error_when_load_palworld_options_type(e):
    QMessageBox.warning(None, "Warning", f"Error loading palworld options type: {e}")


def if_error_when_load_special_options_file(e):
    QMessageBox.warning(None, "Warning", f"Error loading special options file: {e}")


def if_error_when_load_banner_image(e):
    QMessageBox.warning(None, "Warning", f"Error loading banner image: {e}")


def if_error_when_load_translations(e):
    QMessageBox.warning(None, "Warning", f"Error loading translations: {e}")


def if_error_when_load_settings_file(e):
    QMessageBox.warning(None, "Warning", f"Error loading settings file: {e}")


def if_error_when_save_settings_file(e):
    QMessageBox.warning(None, "Warning", f"Error saving settings file: {e}")


def if_save_settings_file_success():
    QMessageBox.information(None, "Information", "Settings file saved successfully.")


def if_error_when_update_settings(option, value):
    QMessageBox.warning(None, "Warning", f"Error updating settings: {option}={value}")


def if_error_when_save_settings_elements_is_none():
    QMessageBox.warning(None, "Warning", f"Error saving settings file: Please try again.")


def if_error_when_load_menu_translation(e):
    QMessageBox.warning(None, "Warning", f"Error loading menu translation: {e}")
