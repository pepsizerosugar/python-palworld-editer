import re

from PyQt5.QtWidgets import QFileDialog

from gui.dialogs.dialogs import show_file
from gui.messageboxs.message_boxs import if_settings_file_is_not_loaded
from utils.translation_utils import load_translations

FILE_PATH = ""
SAVE_PATH = ""


def load_settings_file(self):
    FILE_PATH = show_file(self)
    if FILE_PATH:
        self.options = parse_settings_file(FILE_PATH)
        self.translations = load_translations("PalWorldSettings.json")

        if self.options and self.translations:
            self.show_settings_ui()


def parse_settings_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            options = {}

            # 정규 표현식을 사용하여 설정 항목과 값을 추출
            pattern = r'(\w+)\s*=\s*([0-9.]+|\w+)?'
            matches = re.findall(pattern, content)

            for match in matches:
                option, value = match
                options[option] = float(value) if '.' in value else value

            return options

    except Exception as e:
        print(f"Error parsing settings file: {e}")
        return None


def save_settings_file(self):
    if not FILE_PATH:
        # 사용자가 불러온 설정 파일이 없는 경우 경고 출력
        if_settings_file_is_not_loaded()
        return

    # 대화 상자를 통해 저장할 위치를 선택
    SAVE_PATH, _ = QFileDialog.getSaveFileName(self, 'Save Settings File', '', 'INI Files (*.ini);;All Files (*)')

    if SAVE_PATH:
        pass
