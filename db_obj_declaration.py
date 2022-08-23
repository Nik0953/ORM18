"""
Объявление классов для базы данных
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Region(Base):
    __tablename__ = 'region'
    id_hh = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    in_use = Column(Integer, nullable=True)

    def __init__(self, id_hh, name, in_use):
        self.id_hh = id_hh
        self.name = name
        self.in_use = in_use

    def __str__(self):
        return f'{self.id_hh}: {self.name}: {self.in_use}'


class Town(Base):
    __tablename__ = 'town'
    id_hh = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, id_hh, name):
        self.id_hh = id_hh
        self.name = name

    def __str__(self):
        return f'{self.id_hh}: {self.name}'


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'{self.id}: {self.name}'


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id_hh = Column(Integer, primary_key=True)
    name = Column(String)
    area = Column(Integer, ForeignKey('region.id_hh'))
    town = Column(Integer, ForeignKey('town.id_hh'))
    s_from = Column(Integer)
    s_to = Column(Integer)
    s_currency = Column(String)
    req = Column(String(2048))
    resp = Column(String(2048))
    url = Column(String(256))

    def __init__(self, id_hh, name, area, town, s_from, s_to, s_currency, req, resp, url):
        self.id_hh = id_hh
        self.name = name
        self.area = area
        self.town = town
        self.s_from = s_from
        self.s_to = s_to
        self.s_currency = s_currency
        self.req = req
        self.resp = resp
        self.url = url

    def __str__(self):
        return f'{self.id_hh}: {self.name}: {self.area} __ и далее...'

class VacSkill(Base):
    __tablename__ = 'vac_skill'
    id = Column(Integer, primary_key=True)
    id_vac = Column(Integer, ForeignKey('vacancy.id_hh'))
    id_skill = Column(Integer, ForeignKey('skill.id'))

    def __init__(self, id, id_vac, id_skill):
        self.id = id
        self.id_vac = id_vac
        self.id_skill = id_skill

    def __str__(self):
        return f'{self.id}: vac {self.id_vac}: skill {self.id_skill}'

