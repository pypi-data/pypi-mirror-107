from typing import Dict
from configparser import ConfigParser
# pylint: disable=no-name-in-module
from pydantic import BaseModel
from services_reviews.common_configs import mapping_type


class ReadConf:
    """ Читаем конфиг ini """
    _configparsers: Dict[str, ConfigParser] = {}
    _config_objects: Dict[str, BaseModel] = {}

    @classmethod
    def read(cls, type_file, conf_dir):
        # todo: change to read_parsed if you like it
        _confparser = ConfigParser()
        file_dir = conf_dir
        _confparser.read(file_dir)
        cls._configparsers[type_file] = _confparser
        cls.validate_config(type_file, mapping_type[conf_dir])
        return _confparser

    @classmethod
    def read_parsed(cls, conf_dir):
        cls.read(conf_dir, conf_dir)    # ключ = имя директории (можно переделать и брать только суффикс)
        return cls.get_parsed(conf_dir)

    @classmethod
    def get(cls, type_file, *args, **kw):
        # todo: change to get_parsed id you like it
        return cls._configparsers[type_file].get(*args, **kw)

    @classmethod
    def get_parsed(cls, type_file: str):
        return cls._config_objects[type_file]

    @classmethod
    def validate_config(cls, type_file: str, type_config: BaseModel):
        d = cls.to_dict(type_file)
        cls._config_objects[type_file] = type_config.parse_obj(d)

    @classmethod
    def to_dict(cls, type_file: str):
        d = {}
        for section in cls._configparsers[type_file].sections():
            d[section] = dict(cls._configparsers[type_file][section])
        return d
