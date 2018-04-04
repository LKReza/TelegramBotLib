# coding=utf8
import copy


class ObjectResult(object):
    def __init__(self, data):
        self.data = None
        self.__serialize(data)
        self.dict_data = data

    def __serialize(self, data):
        if type(data) == dict:
            setattr(self, 'data', self.__get_dict_attr(data))
        elif type(data) == list:
            setattr(self, 'data', self.__get_list_attr(data))
        else:
            setattr(self, 'data', data)

    def __get_dict_attr(self, data):
        sub_obj = SubObjectResult()

        for key, value in data.items():
            if type(value) == dict:
                setattr(sub_obj, key, self.__get_dict_attr(value))
            elif type(value) == list:
                setattr(sub_obj, key, self.__get_list_attr(value))
            else:
                setattr(sub_obj, key, value)

        return sub_obj

    def __get_list_attr(self, data):
        lst = []
        for value in data:
            if type(value) == dict:
                lst.append(self.__get_dict_attr(value))
            elif type(value) == list:
                lst.append(self.__get_list_attr(value))
            else:
                lst.append(value)
        return lst


class SubObjectResult(object):
    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item, default=None):
        return getattr(self, item, default)

    def __contains__(self, item):
        return hasattr(self, item)
