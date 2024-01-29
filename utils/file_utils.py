import json
import re

import qtmodern.windows

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.dialogs.dialogs import dialog_for_load_settings_file, dialog_for_save_settings_file
from gui.messageboxs.message_boxs import if_settings_file_is_not_loaded, if_error_when_load_settings_file, \
    if_error_when_save_settings_file, if_save_settings_file_success, if_error_when_save_settings_elements_is_none, \
    if_load_settins_file_is_finished, if_error_when_load_menu_translation, \
    if_error_when_load_palworld_options_type, if_error_when_load_metadata
from gui.utils.gui_utils import resize_windows, set_editor_table_widget_data, move_center, load_settings_from_table
from utils.translation_utils import load_option_description_translations_with_xlsx


def init_file_utils():
    load_metadata()
    load_translations()
    load_palworld_options_type()


def load_metadata():
    try:
        DataElements.metadata = {}
        try:
            with open("resources/config/meta.json", 'r', encoding='utf-8') as file:
                DataElements.metadata = json.loads(file.read())
        except FileExistsError:
            pass
    except Exception as e:
        if_error_when_load_metadata(e)


def load_translations():
    try:
        DataElements.menu_translations = {}
        DataElements.options_translations = []
        try:
            with open("resources/config/translation/menu.json", 'r', encoding='utf-8') as file:
                DataElements.menu_translations = json.loads(file.read())
                DataElements.options_translations = load_option_description_translations_with_xlsx()
        except FileExistsError:
            pass
    except Exception as e:
        if_error_when_load_menu_translation(e)


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


def load_settings_file(window):
    DataElements.settings_file_path = dialog_for_load_settings_file(window)
    if DataElements.settings_file_path:
        DataElements.palworld_options = parse_settings_file()
        if DataElements.is_first_load:
            UIElements.browse_window.close()
            set_editor_table_widget_data()
            UIElements.editor_window.setDisabled(False)
            UIElements.editor_window = qtmodern.windows.ModernWindow(UIElements.editor_window)
            UIElements.editor_window.show()
            resize_windows()
            move_center(UIElements.editor_window)
            if_load_settins_file_is_finished()
            DataElements.is_first_load = False
        else:
            set_editor_table_widget_data()


def parse_settings_file():
    try:
        with open(DataElements.settings_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            options = {}

            pattern = r"\(([\w\W]*?)\)"
            matches = re.search(pattern, content).group(1).split(",")
            matches = [match.split("=") for match in matches]
            matches = [(name, value.strip('\"')) for name, value in matches]

            for match in matches:
                option, value = match
                options.update({option: value})
            return options

    except Exception as e:
        if_error_when_load_settings_file(e)
        return None


def save_settings_file():
    check_is_settings_loaded()

    save_path = DataElements.settings_file_path

    if save_path:
        save_file(save_path)


def save_as_settings_file():
    check_is_settings_loaded()

    save_path = dialog_for_save_settings_file(UIElements.editor_window)

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
