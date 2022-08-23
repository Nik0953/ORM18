"""
Вспомогательный модуль для получения
данных из файлов json
"""

import json


def json_data_to_obj(file_json_name):
    """
    Функция читает данные из файла json
    и возвращает список словарей
    для перенесения данных в новую базу данных
    :param file_json_name:
    :return: dict_lst - список словарей c с данными
    """

    with open(file_json_name, 'r') as f:
        dict_lst = json.load(f)
        f.close()

    return dict_lst
