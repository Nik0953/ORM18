"""
Вспомогательный модуль
перекачивает данные из старой базы vac_hh.db
в json, чтобы потом достать оттуда для новой базы.
"""

import sqlite3
import json

# старая база
dbase_old_name = 'data/vac_hh.db'

conn = sqlite3.connect(dbase_old_name)
cursor = conn.cursor()


# читаем все названия всех таблиц из старой базы
cursor.execute('select * from sqlite_master')
tab_tuple_lst = cursor.fetchall()
tab_names = [t[1] for t in tab_tuple_lst
             if t[0] == 'table' and t[1] != 'sqlite_sequence']

for tab in tab_names:
    # получаем имена полей для каждой таблицы
    cursor.execute('pragma table_info(%s)' % (tab))
    fields_tuple_lst = cursor.fetchall()
    fields_lst = [s[1] for s in fields_tuple_lst]

    # читаем всю информацию из таблицы
    req = f'select * from {tab}'
    cursor.execute(req)
    data_tuple_lst = cursor.fetchall()

    # создаем список словарей
    tab_dict_lst = []
    for rec in data_tuple_lst:
        tab_dict = {}
        for i in range(len(fields_lst)):
            tab_dict[fields_lst[i]] = rec[i]
        tab_dict_lst.append(tab_dict)

        #  имя выходного файла
        output_file_name = f'data/old_data_json/{tab}.json'

        # записываем все записи из таблицы в отдельный файл
        with open(output_file_name, 'w') as f:
            json.dump(tab_dict_lst, f, ensure_ascii=False)
            f.close()

# *******  Завершение работы с таблицами   *******
#    commit the changes to db
conn.commit()
#    close the connection
conn.close()
