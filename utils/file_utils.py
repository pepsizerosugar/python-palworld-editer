import re

from PyQt5.QtWidgets import QFileDialog

from gui.dialogs.dialogs import show_file
from gui.messageboxs.message_boxs import if_settings_file_is_not_loaded, if_error_when_load_settings_file, \
    if_error_when_save_settings_file
from gui.utils.gui_utils import set_table_widget_data, resize_windows
from utils.translation_utils import load_translations


def load_settings_file(self):
    file_path = show_file(self)
    if file_path:
        self.options = parse_settings_file(file_path)
        self.translations = load_translations("PalWorldSettings.json")

        if self.options and self.translations:
            if not self.central_widget:
                self.init_central_widget()
                set_table_widget_data(self, True)
            else:
                set_table_widget_data(self, False)


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
        if_error_when_load_settings_file(e)
        return None


def save_settings_file(self):
    # 사용자가 불러온 설정 파일이 없는 경우 경고 출력
    if not self.options:
        if_settings_file_is_not_loaded(self)
        return

    # 대화 상자를 통해 저장할 위치를 선택
    save_path, _ = QFileDialog.getSaveFileName(self, 'Save Settings File', '', 'INI Files (*.ini);;All Files (*)')

    if save_path:
        try:
            with open(save_path, 'w') as file:
                file.write("[/Script/Pal.PalGameWorldSettings]\n")
                file.write("OptionSettings=(")

                for option, value in self.options.items():
                    if value:
                        file.write(f"{option}={value},")
                    else:
                        value = '""'

                file.write(")")
        except Exception as e:
            if_error_when_save_settings_file(e)
