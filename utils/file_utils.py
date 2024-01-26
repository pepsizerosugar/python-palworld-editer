import re

from PyQt5.QtWidgets import QFileDialog

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.dialogs.dialogs import show_file
from gui.messageboxs.message_boxs import if_settings_file_is_not_loaded, if_error_when_load_settings_file, \
    if_error_when_save_settings_file
from gui.utils.gui_utils import resize_windows, set_table_widget_data, move_center
from gui.widgets.palworld_settings_widget import PalWorldSettingsWidget
from utils.translation_utils import load_translations


def load_settings_file():
    file_path = show_file()
    if file_path:
        DataElements.palworld_options = parse_settings_file(file_path)
        DataElements.options_translations = load_translations("PalWorldSettings.json")
        # 첫 설정 파일을 불러오는 경우 설정 위젯 생성
        if DataElements.is_first_load:
            UIElements.browse_window.close()
            UIElements.settings_central_widget = PalWorldSettingsWidget()
            set_table_widget_data()
            resize_windows()
            move_center(UIElements.settings_window)
        else:
            # 설정 위젯이 이미 생성된 경우 설정 위젯의 테이블 위젯 데이터만 갱신
            pass


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
        if_settings_file_is_not_loaded()
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
