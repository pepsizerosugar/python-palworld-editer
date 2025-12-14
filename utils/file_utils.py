"""Utility helpers for reading, writing, and preparing Palworld settings files."""

import json
import re
from typing import Dict, List

import qtmodern.windows
from PyQt5.QtWidgets import QMainWindow

from gui.dataclass.data_elements import DataElements
from gui.dataclass.ui_elements import UIElements
from gui.dialogs.dialogs import dialog_for_load_settings_file, dialog_for_save_settings_file
from gui.messageboxs.message_boxs import (
    if_error_when_load_menu_translation,
    if_error_when_load_metadata,
    if_error_when_load_palworld_options_type,
    if_error_when_load_settings_file,
    if_error_when_save_settings_elements_is_none,
    if_error_when_save_settings_file,
    if_load_settins_file_is_finished,
    if_save_settings_file_success,
    if_settings_file_is_not_loaded,
)
from gui.utils.gui_utils import (
    load_settings_from_table,
    move_center,
    resize_windows,
    set_editor_table_widget_data,
)
from utils.translation_utils import load_option_description_translations

def init_file_utils() -> None:
    """Initialize configuration data in memory before launching the UI."""

    load_metadata()
    load_translations()
    load_palworld_options_type()


def load_metadata() -> None:
    """Load static metadata such as window titles from disk.

    The metadata file is optional. Missing files are ignored while other
    exceptions are surfaced via a user-facing message box.
    """

    try:
        DataElements.metadata = {}
        try:
            with open("resources/config/meta.json", "r", encoding="utf-8") as file:
                DataElements.metadata = json.loads(file.read())
        except FileNotFoundError:
            pass
    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_load_metadata(exc)


def load_translations() -> None:
    """Load menu and option translation dictionaries from JSON files.

    Missing files are tolerated to keep the application usable while surfacing
    other errors to the operator.
    """

    try:
        DataElements.menu_translations = {}
        DataElements.options_translations = {}
        try:
            with open("resources/config/translation/menu.json", "r", encoding="utf-8") as file:
                DataElements.menu_translations = json.loads(file.read())
                DataElements.options_translations = load_option_description_translations()
        except FileNotFoundError:
            pass
    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_load_menu_translation(exc)


def load_palworld_options_type() -> None:
    """Populate the option type map used to render the editor widgets."""

    try:
        DataElements.palworld_options_type = {}
        try:
            with open("resources/config/options_type.json", "r", encoding="utf-8") as file:
                DataElements.palworld_options_type = json.loads(file.read())
        except FileNotFoundError:
            pass
    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_load_palworld_options_type(exc)


def load_settings_file(window: QMainWindow) -> None:
    """Open a file dialog and load a Palworld settings file.

    Args:
        window: Parent window used for the file dialog.
    """

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


def parse_settings_file() -> Dict[str, str]:
    """Parse the selected ``PalWorldSettings.ini`` into a dictionary.

    Returns:
        dict: Parsed option names mapped to string values. Returns an empty
        dictionary if the file does not contain expected contents.
    """

    try:
        with open(DataElements.settings_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            options: Dict[str, str] = {}

            def split_with_brackets(value: str) -> List[str]:
                """Split a string on commas while respecting parentheses and quotes.

                Args:
                    value (str): Raw ``OptionSettings`` content to tokenize.

                Returns:
                    List[str]: Segments broken on commas while preserving bracketed
                    and quoted groupings.
                """

                parts: List[str] = []
                current: List[str] = []
                depth: int = 0
                in_quote: bool = False

                for char in value:
                    if char == '"':
                        in_quote = not in_quote
                        current.append(char)
                        continue

                    if char == "(" and not in_quote:
                        depth += 1
                    elif char == ")" and not in_quote and depth > 0:
                        depth -= 1

                    if char == "," and not in_quote and depth == 0:
                        parts.append("".join(current))
                        current = []
                    else:
                        current.append(char)

                if current:
                    parts.append("".join(current))
                return parts

            option_match = re.search(r"OptionSettings\s*=\s*\(", content)
            if not option_match:
                return options

            option_content = content[option_match.end() - 1 :]
            if not option_content.startswith("(") or option_content.rfind(")") == -1:
                return options

            matches = split_with_brackets(option_content[1: option_content.rfind(")")])
            parsed_pairs = [
                pair for pair in (match.split("=", 1) for match in matches if match) if len(pair) == 2
            ]
            normalized_pairs = [
                (
                    name.strip(),
                    value.strip().strip("\""),
                )
                for name, value in parsed_pairs
            ]

            for option, value in normalized_pairs:
                if option:
                    options[option] = value
            return options

    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_load_settings_file(exc)
        return {}


def save_settings_file() -> None:
    """Save the current settings back to the original path if available."""

    check_is_settings_loaded()
    save_path = DataElements.settings_file_path
    if save_path:
        save_file(save_path)


def save_as_settings_file() -> None:
    """Save the current settings to a new file chosen via dialog."""

    check_is_settings_loaded()
    save_path = dialog_for_save_settings_file(UIElements.editor_window)
    if save_path:
        save_file(save_path)


def check_is_settings_loaded() -> bool:
    """Validate that a settings file has been loaded before saving.

    Returns:
        bool: ``True`` when settings exist; otherwise ``False`` with a warning.
    """

    if not DataElements.palworld_options:
        if_settings_file_is_not_loaded()
        return False
    return True


def save_file(save_path: str) -> None:
    """Write the in-memory options to disk.

    Args:
        save_path (str): Destination file path for the settings file.
    """

    try:
        DataElements.palworld_options_to_save = load_settings_from_table()
        if DataElements.palworld_options_to_save:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write("[/Script/Pal.PalGameWorldSettings]\n")
                file.write("OptionSettings=(")

                for option, value in DataElements.palworld_options_to_save.items():
                    if value or isinstance(value, bool):
                        option_type = DataElements.palworld_options_type[option]
                        match option_type:
                            case "str":
                                file.write(f"{option}=\"{value}\",")
                            case _:
                                file.write(f"{option}={value},")
                    else:
                        file.write(f"{option}=\"{value}\",")
                file.seek(file.tell() - 1, 0)
                file.write(")")
            if_save_settings_file_success()
        else:
            if_error_when_save_settings_elements_is_none()
    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_save_settings_file(exc)
