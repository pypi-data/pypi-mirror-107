# coding: utf-8

import os
import yaml
import json
import logging
from jsonschema import validate, ValidationError
from copy import deepcopy


class config(object):

    def __init__(self, desc):
        # 初始化
        self._name = ''
        self._value = {}
        self._desc = {}
        self._default = {}
        # 根据不同的参数进行构建实例
        if isinstance(desc, str):
            filename = desc + '.desc'
            desc_tmp = config.load(filename)
            self._name = desc_tmp['name']
            self._desc = desc_tmp['schema']
            self._default = desc_tmp['default']
        else:
            if isinstance(desc, dict):
                self._name = desc['name']
                self._desc = desc['schema']
                self._default = desc['default']
            else:
                raise TypeError('Parameter "desc" should be str or dict.')
        self.set_default()

    def validate(self):
        try:
            validate(instance=self._value, schema=self._desc)
            return True
        except ValidationError:
            return False

    def load_config(self, config_filename):
        old_value = self._value.copy()
        self._value = config.load(config_filename)
        if self.validate():
            pass
        else:
            self._value = old_value
            raise ValueError('Value for setting is invalid.')

    @staticmethod
    def load(ori_filename):
        obj_json = None
        filename = os.path.join(os.getcwd(), ori_filename)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                obj_json = yaml.safe_load(f)
                logging.info('Succeeded reading file "' + filename + '".')
        else:
            logging.warning(str(filename) + ' is not found.')
        return obj_json

    def dump(self, dist_filename=None):
        if self.validate():
            config_filename = self._name + '.cfg'
            if dist_filename is None:
                pass
            else:
                config_filename = dist_filename
            filename = os.path.join(os.getcwd(), config_filename)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self._value, f, indent=4)
        else:
            raise AssertionError('Value of "' + self._name + '" is invalid.')

    def __getitem__(self, item):
        if item in self._value:
            return self._value[item]
        else:
            raise KeyError('Key "' + item + '" is not found in config object "' + self._name + '".')

    def __setitem__(self, key, value):
        if key in self._value:
            t = type(self._default[key])
            if isinstance(value, t):
                old_value = self._value.copy()
                self._value[key] = value
                if self.validate():
                    pass
                else:
                    self._value = old_value
                    raise ValueError('Value for setting is invalid.')
            else:
                raise ValueError('Value for setting should be ' + str(t) + '.')
        else:
            raise KeyError('Key "' + key + '" is not found in config object "' + self._name + '".')

    def __repr__(self):
        return self._value.__repr__()

    def __contains__(self, item):
        return item in self._value

    def is_default(self, key: str = None):
        if key is None:
            return self._value == self._default
        else:
            return self._value[key] == self._default[key]

    def set_default(self):
        self._value = deepcopy(self._default)
