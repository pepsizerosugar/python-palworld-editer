import json
import os

import pandas as pd

script_dir = os.path.dirname(__file__)
excel_path = os.path.join(script_dir, 'translations.xlsx')
json_path = os.path.join(script_dir, 'translations.json')


def excel_to_json(excel_file_path, json_file_path):
    df = pd.read_excel(excel_file_path, header=0)
    json_data = df.to_dict(orient='records')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)


excel_to_json(excel_path, json_path)
