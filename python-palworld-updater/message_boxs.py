from PyQt5.QtWidgets import QMessageBox


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


def if_update_is_not_needed():
    QMessageBox.information(None, f"Information", "Update is not needed."
                                                  "\nShutting down the updater.")
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
