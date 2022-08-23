"""
Модуль создает новую базу данных
с помощью ОRM
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# для получения данных из файлов json
from get_json_data import *

#  здесь объявляются все классы данных
from db_obj_declaration import *

engine = create_engine('sqlite:///data/new_data/new_hh.db', echo=True)

# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии
# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# заполняем таблицу регионов
reg_dict_lst = json_data_to_obj('data/old_data_json/region.json')

reg_lst = []
for rd in reg_dict_lst:
    region = Region(rd['id_hh'], rd['name'], rd['in_use'])
    reg_lst.append(region)

session.add_all(reg_lst)


# заполняем таблицу населенных пунктов
town_dict_lst = json_data_to_obj('data/old_data_json/town.json')

town_lst = []
for t in town_dict_lst:
    town = Town(t['id_hh'], t['name'])
    town_lst.append(town)

session.add_all(town_lst)


# заполняем таблицу ключевых навыков
skill_dict_lst = json_data_to_obj('data/old_data_json/skill.json')

sk_lst = []
for s in skill_dict_lst:
    skill = Skill(s['id'], s['name'])
    sk_lst.append(skill)

session.add_all(sk_lst)


# заполняем таблицу вакансий
vacancy_dict_lst = json_data_to_obj('data/old_data_json/vacancy.json')

vac_lst = []
for v in vacancy_dict_lst:
    vacancy = Vacancy(v['id_hh'], v['name'], v['area'],
                      v['town'], v['s_from'], v['s_to'],
                      v['s_currency'], v['req'], v['resp'], v['url'])
    vac_lst.append(vacancy)

session.add_all(vac_lst)

# заполняем таблицу связей
vs_dict_lst = json_data_to_obj('data/old_data_json/vac_skill.json')

vs_lst = []
for vs in vs_dict_lst:
    vac_sk = VacSkill(vs['id'], vs['id_vac'], vs['id_skill'])
    vs_lst.append(vac_sk)

session.add_all(vs_lst)


session.commit()

