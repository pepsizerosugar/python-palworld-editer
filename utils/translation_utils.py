"""Utilities for loading and switching language translations."""

import json
from typing import Dict

from gui.dataclass.data_elements import DataElements
from gui.messageboxs.message_boxs import if_error_when_load_translations


def change_translation_code(index: int) -> None:
    """Update the active translation code by combo-box index.

    Args:
        index (int): Selected index from the translation combo box.
    """

    if DataElements.translation_code_list and 0 <= index < len(DataElements.translation_code_list):
        DataElements.translation_code = DataElements.translation_code_list[index]


def load_option_description_translations() -> Dict[str, Dict[str, str]]:
    """Load option description translations from the JSON source.

    Returns:
        dict: Mapping of option names to localized description dictionaries.
    """

    DataElements.translation_code_list = []
    try:
        translation_file_path = "resources/config/translation/translations.json"
        with open(translation_file_path, "r", encoding="utf-8") as file:
            translations: Dict[str, Dict[str, str]] = json.load(file)

        if translations:
            first_row = next(iter(translations.values()))
            DataElements.translation_code_list = list(first_row.keys())

        return translations

    except Exception as exc:  # pylint: disable=broad-except
        if_error_when_load_translations(exc)
        return {}
