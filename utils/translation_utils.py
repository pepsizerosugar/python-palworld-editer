import json

from gui.dataclass.data_elements import DataElements
from gui.messageboxs.message_boxs import if_error_when_load_translations


def change_translation_code(index):
    DataElements.translation_code = DataElements.translation_code_list[index]


def load_translations():
    try:
        translation_file_path = f"resources/config/translations.json"
        with open(translation_file_path, 'r', encoding='utf-8') as file:
            translations = json.load(file)

        return translations

    except Exception as e:
        if_error_when_load_translations(e)
        return None


def convert_translation_list_to_dict(translations):
    return {entry["parameter"]: entry for entry in translations}
