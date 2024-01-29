from gui.dataclass.data_elements import DataElements
from gui.messageboxs.message_boxs import if_error_when_load_translations


def change_translation_code(index):
    DataElements.translation_code = DataElements.translation_code_list[index]


def load_option_description_translations_with_xlsx():
    DataElements.translation_code_list = []
    try:
        translation_file_path = "resources/config/translation/translations.xlsx"
        import pandas as pd
        translations = pd.read_excel(translation_file_path, engine='openpyxl').to_dict('records')
        DataElements.translation_code_list = list(translations[0].keys())[1:]
        return convert_translation_list_to_dict(translations)

    except Exception as e:
        if_error_when_load_translations(e)
        return None


def convert_translation_list_to_dict(translations):
    return {entry["parameter"]: entry for entry in translations}
