"""
Вспомогательный модуль готовит информацию для
представления на web-странице
"""

import json

# ======================================
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# для получения данных из файлов json
from get_json_data import *

#  здесь объявляются все классы данных
from db_obj_declaration import *



# ======================================

def get_web_info():
    """
    Функция возвращает четыре словаря:

    словарь условий запроса к hh.ru:
    req_dict = {
                {"vac_regs": cписок строк - названий регионов РФ, в которых ищем вакансии
                 "key_words": ключевые слова поиска
                 "days_vac_valid": актуальность вакансии, дней
                 "with_salary": обязательно ли с указанием заработной платы
                 }
    словарь регионов, в которых проводился поиск
    reg_active_dict{'имя региона': код_города_hh}

    словарь результатов поиска
    search_result_dict = {
                 'vac_number': сколько найдено вакансий
                 'sal_max': максимум оплаты по всем полям всех вакансий
                 }

    словарь ключевых слов для вакансии
    skill_dict = {
                 'name': слово
                 'id':   id
    """

    engine = create_engine('sqlite:///data/new_data/new_hh.db', echo=False)

    # Создание таблицы
    Base.metadata.create_all(engine)

    # Создание сессии
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()


    # читаем из файла json условия запроса вакансий
    req_dict = {}
    with open('data/request_dict.json', 'r') as f:
        req_dict = json.load(f)
        f.close()

    # словарь регионов, в которых проводился поиск
    reg_active_dict = {'ВСЕ': 0}
    regs = session.query(Region).filter(Region.in_use==1)
    for r in regs:
        reg_active_dict[r.name] = r.id_hh


    # формируем словарь требований к должности
    skill_dict = {'БЕЗ ТРЕБОВАНИЙ': 0}
    skills = session.query(Skill)
    for sk in skills:
        skill_dict[sk.name] = sk.id

    # общая информация о полученных вакансиях:
    search_result_dict = {}
    # максимальная заработная плата
    s_from_max = session.query(func.max(Vacancy.s_from)).scalar()
    s_to_max = session.query(func.max(Vacancy.s_to)).scalar()
    search_result_dict['sal_max'] = max(s_from_max, s_to_max)
    # сколько всего вакансий
    search_result_dict['vac_number'] = session.query(Vacancy).count()


    return req_dict, reg_active_dict, search_result_dict, skill_dict




def get_vac_info(where_to_find=0, what_skills=0,sal_min=0):
    """
    выдает список словарей-вакансий,
    информация о каждой вакансии усеченная:
        id
        название
        заработная плата
        регион,
        населенный пункт,
        key-skills вакансии (строкой)
        url
    :param: filter - словарь с ограничениями для поиска

    :param where_to_find: код региона для выборки
    :param what_skills: код скил для выборки
    :param sal_min: минимальная заработная плата
    :return: список словарей вакансии
    """

    engine = create_engine('sqlite:///data/new_data/new_hh.db', echo=False)

    # Создание таблицы
    Base.metadata.create_all(engine)

    # Создание сессии
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    # Полный список вакансий
    vacancies = session.query(Vacancy.id_hh, Vacancy.name, Region.name, Town.name, Vacancy.s_from, Vacancy.s_to,
                              Vacancy.s_currency, Vacancy.url).filter(Vacancy.area == Region.id_hh, Vacancy.town == Town.id_hh)

    # Отбор по ключевому навыку
    if(what_skills):
        vacancies = vacancies.filter(VacSkill.id_vac == Vacancy.id_hh, VacSkill.id_skill == what_skills)

    # Отбор по заработной плате
    if (sal_min):
        vacancies = vacancies.filter((Vacancy.s_from >= sal_min)|(Vacancy.s_to >= sal_min))

    # Отбора по региону
    if (where_to_find):
        vacancies = vacancies.filter(Vacancy.area == where_to_find)


    # собираем все данные в список красивых словарей для публикации
    vac_lst = vacancies.all()
    vac_dict_lst = []

    for vac in vac_lst:

        vac_dict={}
        id = vac[0]
        vac_dict['id'] = vac[0]
        vac_dict['name'] = vac[1]
        vac_dict['reg'] = vac[2]
        vac_dict['town'] = vac[3]
        vac_dict['s_from'] = vac[4]
        vac_dict['s_to'] = vac[5]
        vac_dict['cur'] = vac[6]
        vac_dict['url'] = vac[7]

        # для публикации - создаем строку со всеми ключевыми словами
        # (не только запрошенными) всех вакансий
        sk_lst = session.query(VacSkill.id_vac, Skill.name).filter(Skill.id == VacSkill.id_skill, VacSkill.id_vac == vac[0]).all()
        txt_skill = '/'
        for s in sk_lst:
            txt_skill += s[1] + '/'

        vac_dict['skill'] = txt_skill

        vac_dict_lst.append(vac_dict)


    return vac_dict_lst

