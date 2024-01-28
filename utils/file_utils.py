import json
import re

import qtmodern.windows

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.dialogs.dialogs import dialog_for_load_settings_file, dialog_for_save_settings_file
from gui.messageboxs.message_boxs import if_settings_file_is_not_loaded, if_error_when_load_settings_file, \
    if_error_when_save_settings_file, if_save_settings_file_success, if_error_when_save_settings_elements_is_none, \
    if_load_settins_file_is_finished, if_error_when_load_special_options_file, if_error_when_load_menu_translation, \
    if_error_when_load_palworld_options_type
from gui.utils.gui_utils import resize_windows, set_table_widget_data, move_center, load_settings_from_table
from utils.translation_utils import load_translations


def load_palworld_options_type():
    try:
        DataElements.palworld_options_type = {}
        try:
            with open("resources/config/options_type.json", 'r', encoding='utf-8') as file:
                DataElements.palworld_options_type = json.loads(file.read())
        except FileExistsError:
            pass
    except Exception as e:
        if_error_when_load_palworld_options_type(e)


def load_special_options_file():
    try:
        DataElements.special_palworld_options = {}
        DataElements.special_settings_file_path = "resources/config/special_options.json"
        try:
            with open(DataElements.special_settings_file_path, 'r', encoding='utf-8') as file:
                DataElements.special_palworld_options = json.loads(file.read())
        except FileExistsError:
            pass
    except Exception as e:
        if_error_when_load_special_options_file(e)


def load_settings_file(window):
    load_special_options_file()
    load_palworld_options_type()
    DataElements.settings_file_path = dialog_for_load_settings_file(window)
    if DataElements.settings_file_path:
        DataElements.palworld_options = parse_settings_file(DataElements.settings_file_path)
        DataElements.options_translations = load_translations()
        if DataElements.is_first_load:
            UIElements.settings_window.setDisabled(False)
            UIElements.settings_window = qtmodern.windows.ModernWindow(UIElements.settings_window)
            UIElements.settings_window.show()
            UIElements.browse_window.close()
            set_table_widget_data()
            resize_windows()
            move_center(UIElements.settings_window)
            DataElements.is_first_load = False
            if_load_settins_file_is_finished()
        else:
            set_table_widget_data()


def parse_settings_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            options = {}

            pattern = r"\(([\w\W]*?)\)"
            matches = re.search(pattern, content).group(1)

            pattern = r"(\w+)\s*=\s*\"?([\w\W]*?)\"?\s*,"
            matches = re.findall(pattern, matches)

            for match in matches:
                option, value = match
                options.update({option: value})
            return options

    except Exception as e:
        if_error_when_load_settings_file(e)
        return None


def load_menu_translation():
    try:
        DataElements.menu_translations = {}
        DataElements.translation_code_list = []
        try:
            with open("resources/config/menu.json", 'r', encoding='utf-8') as file:
                DataElements.menu_translations = json.loads(file.read())
                DataElements.translation_code_list = list(DataElements.menu_translations["translation_code"])
        except FileExistsError:
            pass
    except Exception as e:
        if_error_when_load_menu_translation(e)


def save_settings_file():
    check_is_settings_loaded()

    save_path = DataElements.settings_file_path

    if save_path:
        save_file(save_path)


def save_as_settings_file():
    check_is_settings_loaded()

    save_path = dialog_for_save_settings_file(UIElements.settings_window)

    if save_path:
        save_file(save_path)


def check_is_settings_loaded():
    if not DataElements.palworld_options:
        if_settings_file_is_not_loaded()
        return False
    else:
        return True


def save_file(save_path):
    try:
        DataElements.palworld_options_to_save = load_settings_from_table()
        if DataElements.palworld_options_to_save:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write("[/Script/Pal.PalGameWorldSettings]\n")
                file.write("OptionSettings=(")

                for option, value in DataElements.palworld_options_to_save.items():
                    if value:
                        option_type = DataElements.palworld_options_type[option]
                        match option_type:
                            case "str":
                                file.write(f"{option}=\"{value}\",")
                            case _:
                                file.write(f"{option}={value},")
                    else:
                        if option == "DeathPenalty":
                            file.write(f"{option}=\"{value}\",")
                        else:
                            file.write(f"{option}="",")
                file.seek(file.tell() - 1, 0)
                file.write(")")
            if_save_settings_file_success()
        else:
            if_error_when_save_settings_elements_is_none()
    except Exception as e:
        if_error_when_save_settings_file(e)
