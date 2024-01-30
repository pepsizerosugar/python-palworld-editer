import os
import shutil
import time
import urllib.request
import zipfile

import psutil
import requests

from message_boxs import if_error_when_check_version_with_request, if_required_update, if_recommended_update, \
    if_error_when_mkdr_update_folder, if_error_when_check_update_files_with_request, if_error_when_unzip_update_files, \
    if_error_when_kill_process, if_error_when_update_files, if_update_finished

MAJOR_UPDATE = 0
RECOMMENDED_UPDATE = 1
PATCH_UPDATE = 2


class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def get_running_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        return os.getcwd()


class Updater:
    def __init__(self):
        self.current_version = self.get_current_version_at_startup()
        self.releases = None
        self.latest_version = Version(None, None, None)
        self.dir_path = get_running_directory()

    @staticmethod
    def get_current_version_at_startup():
        if "--current_version" in sys.argv:
            current_version_index = sys.argv.index("--current_version") + 1
            if current_version_index < len(sys.argv):
                current_version = sys.argv[current_version_index]
                version_parts = map(int, current_version.split("."))
                return Version(*version_parts)
        return Version(1, 0, 0)

    def check_version(self):
        try:
            self.releases = requests.get(
                "https://api.github.com/repos/pepsizerosugar/python-palworld-editer/releases/latest").json()
            _version = self.releases.get("tag_name")
            version_parts = map(int, _version.split("."))
            self.latest_version = Version(*version_parts)
        except Exception as e:
            if_error_when_check_version_with_request(e)

        self.handle_update(self.get_update_type())

    def get_update_type(self):
        if self.current_version.major < self.latest_version.major:
            return MAJOR_UPDATE
        elif self.current_version.minor < self.latest_version.minor:
            return RECOMMENDED_UPDATE
        elif self.current_version.patch < self.latest_version.patch:
            return PATCH_UPDATE

    def handle_update(self, update_type):
        if update_type == MAJOR_UPDATE:
            if_required_update(self)
        elif update_type == RECOMMENDED_UPDATE or update_type == PATCH_UPDATE:
            if_recommended_update(self)
        else:
            with open('update_not_needed.txt', 'w') as f:
                f.write('update_not_needed')
            sys.exit()

    def update_app(self):
        try:
            with open('shutdown_request.txt', 'w') as f:
                f.write('shutdown')
            while True:
                try:
                    for proc in psutil.process_iter():
                        if proc.name() == "PalEditor.exe":
                            proc.kill()
                            proc.wait(10)
                            break
                        time.sleep(0.25)
                    break
                except Exception as e:
                    pass
        except Exception as e:
            if_error_when_kill_process(e)
        finally:
            os.remove('shutdown_request.txt')

        _release = self.releases.get("assets")[0].get("browser_download_url")

        try:
            update_directory = os.path.join(self.dir_path, "update")
            if not os.path.exists(update_directory):
                os.makedirs(update_directory)
            else:
                shutil.rmtree(update_directory)
                os.makedirs(update_directory)
        except Exception as e:
            if_error_when_mkdr_update_folder(e)
            return

        try:
            current_process = psutil.Process(os.getpid())
            for file in current_process.open_files():
                file_handle = file.fd
                try:
                    if file_handle >= 0:
                        os.close(file_handle)
                except OSError as e:
                    pass

            time.sleep(1)

            update_zip_path = os.path.join(update_directory, "update.zip")
            urllib.request.urlretrieve(_release, update_zip_path)
        except Exception as e:
            if_error_when_check_update_files_with_request(e)
            return

        try:
            with zipfile.ZipFile(update_zip_path) as zf:
                zf.extractall(update_directory + "/update")
        except Exception as e:
            if_error_when_unzip_update_files(e)
            return

        try:
            update_files_directory = os.path.join(update_directory, "update")
            for filename in os.listdir(update_files_directory):
                if filename != "update.zip":
                    source_path = os.path.join(update_files_directory, filename)
                    destination_path = os.path.join(self.dir_path, filename)

                    if os.path.exists(destination_path):
                        if os.path.isdir(destination_path):
                            shutil.rmtree(destination_path)
                        else:
                            os.remove(destination_path)
                    shutil.move(source_path, destination_path)
            os.remove(update_zip_path)
            shutil.rmtree(update_files_directory)
            shutil.rmtree(update_directory)
        except Exception as e:
            if_error_when_update_files(e)
            return

        if_update_finished()
        os.startfile(os.path.join(self.dir_path, "PalEditor.exe"))


if __name__ == '__main__':
    import sys
    import qtmodern.styles
    import qtmodern.windows
    from PyQt5 import QtCore
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication

    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resource/icon.ico'))
    qtmodern.styles.dark(app)
    Updater().check_version()
    sys.exit(app.exec_())
