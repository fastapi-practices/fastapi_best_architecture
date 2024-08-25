# !/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import decimal
import json


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# dict to json
def dict_to_json(dic: dict):
    return json.dumps(dic, cls=CJsonEncoder)


# json to dict
def json_to_dict(json_msg):
    dic = json.loads(s=json_msg)
    return dic


# 不格式化的输出ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii(dic: dict, ensure_ascii=False):
    return json.dumps(dic, cls=CJsonEncoder, ensure_ascii=ensure_ascii)


# 格式化排版缩进输出-ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii_indent(dic: dict, ensure_ascii=False):
    return json.dumps(dic, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


def is_json(data):
    """
    检查给定的数据是否为有效的 JSON 字符串。

    :param data: 要检查的数据。
    :return: 如果数据是有效的 JSON 字符串，则返回 True，否则返回 False。
    """
    try:
        json.loads(data)
        return True
    except (TypeError, ValueError):
        return False


def is_dict(data):
    """
    检查给定的数据是否为字典。

    :param data: 要检查的数据。
    :return: 如果数据是字典，则返回 True，否则返回 False。
    """
    return isinstance(data, dict)


# class to dict
def class_to_dict(obj):
    if not obj:
        return None
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dic = {}
            dic.update(o.__dict__)
            obj_arr.append(dic)
        return obj_arr
    else:
        dic = {}
        dic.update(obj.__dict__)
        return dic.get('__data__')


# object to json
def obj_to_json(obj, ensure_ascii=False):
    stu = obj.__dict__  # 将对象转成dict字典
    return json.dumps(obj=stu, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


if __name__ == '__main__':
    dict_info = {'name': '张三', 'age': 18, 'birthday': datetime.datetime.now(), 'money': decimal.Decimal('12.34')}
    # {"name": "\u5f20\u4e09", "age": 18, "birthday": "2022-11-18 13:48:04", "money": 12.34}
    print(dict_to_json(dict_info))

    # {'name': '张三', 'age': 18}
    print(json_to_dict('{"name": "张三", "age": 18}'))

    # {"name": "张三", "age": 18, "birthday": "2022-11-18 13:48:04", "money": 12.34}
    print(dict_to_json_ensure_ascii(dict_info, ensure_ascii=False))

    # {
    #     "name": "张三",
    #     "age": 18,
    #     "birthday": "2022-11-18 13:48:04",
    #     "money": 12.34
    # }
    print(dict_to_json_ensure_ascii_indent(dict_info, ensure_ascii=False))

    # print(obj_to_json(dict_info, ensure_ascii=False))
