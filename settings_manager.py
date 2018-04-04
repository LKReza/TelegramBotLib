# coding=utf8
import os
import json


class SettingsManager(object):
    def __init__(self, name, settings_root_dir):
        self.name = name
        self.settings_dir = os.path.join(
            settings_root_dir,
            name,
            'settings'
        )

        if not os.path.exists(self.settings_dir):
            os.makedirs(self.settings_dir)

        self.mapping = {}
        self.settings = {}

    def load(self, rel_path, name):
        file_path = os.path.join(self.settings_dir, rel_path)

        with open(file_path, 'r') as infile:
            data = infile.read()
            self.settings[name] = json.loads(data)
            self.mapping[name] = rel_path

        self.__set_settings_attr(name, self.settings[name])

    def update(self, name):
        self.load(self.mapping[name], name)

    def dump(self, name):
        file_path = os.path.join(self.settings_dir, self.mapping[name])

        with open(file_path, 'wb') as out:
            out.write(json.dumps(self.settings[name]))

    def create(self, rel_path, name, data):
        self.mapping[name] = rel_path
        file_path = os.path.join(self.settings_dir, self.mapping[name])

        with open(file_path, 'wb') as out:
            out.write(json.dumps(data))
            self.settings[name] = data

        self.__set_settings_attr(name, self.settings[name])

    def load_upsert(self, rel_path, name, data):
        file_path = os.path.join(self.settings_dir, rel_path)
        if not os.path.exists(file_path):
            self.create(rel_path, name, data)
        else:
            self.load(rel_path, name)

    def __set_settings_attr(self, name, value):
        setattr(self, name, value)
