import json
import os

from gui.messageboxs.message_boxs import if_error_when_load_translations


def load_translations(filename):
    try:
        # 번역 파일이 resources/ 폴더에 있다고 가정
        resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources')
        translation_file_path = os.path.join(resources_path, filename)

        with open(translation_file_path, 'r', encoding='utf-8') as file:
            translations = json.load(file)

        return translations

    except Exception as e:
        if_error_when_load_translations(e)
        return None


def convert_translation_list_to_dict(translations):
    # 번역 파일이 리스트일 경우 딕셔너리로 변환하는 함수
    return {entry["parameter"]: entry for entry in translations}


def change_translation_code(self, index):
    self.translation_code = ["ko", "en", "jp"][index]
