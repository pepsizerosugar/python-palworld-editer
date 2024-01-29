import os
import shutil
import sys
import time
import urllib.request
import zipfile

import psutil
import requests

from gui.messageboxs.message_boxs import if_error_when_check_version_with_request, if_required_update, \
    if_recommended_update, if_error_when_check_update_files_with_request, if_error_when_unzip_update_files, \
    if_error_when_mkdr_update_folder, if_update_success, if_error_when_update_files

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


def get_script_directory():
    if getattr(sys, 'frozen', False):  # PyInstaller로 빌드된 경우
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        return os.getcwd()


class VersionChecker:
    def __init__(self):
        self.releases = None
        self.current_version = Version(1, 0, 0)
        self.latest_version = Version(None, None, None)
        self.dir_path = get_script_directory()
        if getattr(sys, 'frozen', False):  # PyInstaller로 빌드된 경우
            self.temp_directory = sys._MEIPASS
        else:  # 일반적인 스크립트 실행인 경우
            self.temp_directory = self.dir_path

    def check_version(self):
        try:
            self.releases = requests.get(
                "https://api.github.com/repos/pepsizerosugar/python-palworld-editer/releases/latest").json()
            _version = self.releases.get("tag_name")
            version_parts = map(int, _version.split("."))
            self.latest_version = Version(*version_parts)
        except Exception as e:
            if_error_when_check_version_with_request(e)
            return

        update_type = self.get_update_type()
        self.handle_update(update_type)

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
        elif update_type == RECOMMENDED_UPDATE:
            if_recommended_update(self)
        elif update_type == PATCH_UPDATE:
            if_recommended_update(self)

    def update_app(self):
        _release = self.releases.get("assets")[0].get("browser_download_url")

        try:
            update_directory = os.path.join(get_script_directory(), "update")
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
                    destination_path = os.path.join(get_script_directory(), filename)

                    if os.path.exists(destination_path):
                        shutil.rmtree(destination_path)
                    shutil.move(source_path, destination_path)

            os.remove(update_zip_path)
            shutil.rmtree(update_files_directory)
        except Exception as e:
            if_error_when_update_files(e)
            return

        # 업데이트 완료 메시지
        if_update_success()
