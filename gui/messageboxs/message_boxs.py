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


def if_error_when_check_version_with_request(e):
    QMessageBox.warning(None, "Warning", f"Error checking version: {e}")


def if_required_update(self):
    reply = QMessageBox.question(None, "Question",
                                 f"Required update available"
                                 f"\nIf you don't update, the program will exit"
                                 f"\n{self.current_version} -> {self.latest_version}",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    if reply == QMessageBox.Yes:
        self.update_app()
    else:
        exit()


def if_recommended_update(self):
    reply = QMessageBox.question(None, "Question",
                                 f"Recommended update available"
                                 f"\nIf you don't update, the program may not work properly"
                                 f"\n{self.current_version} -> {self.latest_version}",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    if reply == QMessageBox.Yes:
        self.update_app()
    else:
        pass


def if_update_finished():
    QMessageBox.information(None, "Information", "Update finished. Please restart the program.")


def if_error_when_check_update_files_with_request(e):
    QMessageBox.warning(None, "Warning", f"Error checking update files: {e}")
    pass


def if_error_when_unzip_update_files(e):
    QMessageBox.warning(None, "Warning", f"Error unzipping update files: {e}")
    pass


def if_error_when_update_files(e):
    QMessageBox.warning(None, "Warning", f"Error updating files: {e}")
    pass


def if_error_when_mkdr_update_folder(e):
    QMessageBox.warning(None, "Warning", f"Error making update folder: {e}")
    pass


def if_error_when_kill_process(e):
    QMessageBox.warning(None, "Warning", f"Error killing process: {e}")
    pass


def if_program_need_to_be_shutdown_for_update():
    QMessageBox.information(None, "Information", "Program need shutdown for update.")
    pass
