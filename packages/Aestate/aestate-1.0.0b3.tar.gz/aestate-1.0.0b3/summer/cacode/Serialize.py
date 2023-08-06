# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        Serialize
# Author:           CACode
# Version:          1.2
# Created:          2021/4/27
# Description:      Main Function:    序列化和反序列化
#                   使用QuerySet[QueryItem]形式存储数据,并通过JsonUtil解析成json
#                   增强版list+dict
# Class List:    JsonUtil -- Json工具集
#               QuerySet -- 返回的结果集对象
#               QueryItem -- 返回的子集对象
# History:
#       <author>        <version>       <time>      <desc>
#       CACode              1.2     2021/4/27    统一序列化器位置
# ------------------------------------------------------------------

from summer.cacode.ReviewJson.JSON import Json
from summer.util.Log import CACodeLog
from summer.cacode import ReviewJson
from datetime import date, datetime
import functools

__version__ = ('Test', 1, 0, 0)
__author__ = 'CACode'
"""
此文件内包含有序列化器所有需要用到的参数
JsonUtil可使用原simplejson部分功能，内嵌simplejson，升级功能包含
- parse(obj,bf,end_load) 解析object类型
- load(obj) 生成字典
"""

__all__ = ['JsonUtil', 'QuerySet', 'PageHelp']


class JsonUtil(Json):
    """作者:CACode 最后编辑于2021/4/27
    Json工具
    JsonUtil.parse(**kwargs):将任意对象解析成json字符串
    JsonUtil.load(**kwargs):将字符串解析成字典
    """

    @staticmethod
    def date_encoder(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return None

    class JsonDateEncoder(ReviewJson.JSONEncoder):
        def default(self, obj):
            return JsonUtil.date_encoder(obj)

    class SimplejsonDateEncoder(ReviewJson.JSONEncoder):
        def default(self, obj):
            return JsonUtil.date_encoder(obj)

    @staticmethod
    def parse(obj, bf=False, end_load=False):
        """作者:CACode 最后编辑于2021/4/27

        将对象转换成字典格式:
            支持:
                dict
                list
                object
                list[object]
                object[list]
                object[list[object]]
                .......

        注意事项:

            bf和end_load同时只能使用一个

            当两者同时存在时,默认使用end_load功能


        :param obj:需要解析的对象
        :param bf:是否需要美化json
        :param end_load:是否需要在最后转成字典格式
        """

        def json_to_str(_obj):
            """
            json转字符串
            """
            json_f = functools.partial(
                JsonUtil.dumps, cls=JsonUtil.JsonDateEncoder)
            json_str = json_f(_obj)
            return json_str

        def parse_list(list_obj):
            """
            解析list数据的json
                放置了递归函数,所以不必担心解析报错或者解析不到位
            """
            obj_dicts = []
            for item in list_obj:
                # 循环集合
                if isinstance(item, list):
                    # 如果是集合则递归
                    obj_dicts.append(parse_list(item))
                elif isinstance(item, tuple):
                    # 如果是tuple元组则转成集合后递归
                    return obj_dicts.append(parse_list(list(item)))
                elif isinstance(item, dict) or isinstance(item, str):
                    # 如果是字典或者字符串,则直接交给obj_dicts填充
                    obj_dicts.append(item)
                elif isinstance(item, object):
                    # 如果是object则交给parse_obj()解析
                    obj_dicts.append(parse_obj(item))
                else:
                    obj_dicts.append(item)
            return obj_dicts

        def parse_obj(_obj) -> str:
            """
            夺命循环递递归
            """
            obj_dicts = []
            if isinstance(_obj, dict):
                _dict = _obj.__dict__
                # 如果是list,则交给parse_list(解决)
                for key, item in _dict.items():
                    obj_dicts.append({
                        key: parse_list(item)
                    })
            elif isinstance(_obj, list):
                # 如果是字典或者字符串,则直接交给obj_dicts填充
                obj_dicts.append(parse_list(_obj))
            # 由于parse_list()中有对于tuple累心的解析,所以不必担心tuple
            elif isinstance(_obj, str):
                # 如果是字典或者字符串,则直接交给obj_dicts填充
                obj_dicts = _obj
            else:
                # 如果不是list类型,则直接解析成字典
                try:
                    obj_dicts = _obj.__dict__
                except AttributeError as e:
                    obj_dicts = _obj
                    # 异常警告，抛出
            return obj_dicts

        def parse_dict(_obj):
            """作者:CACode 最后编辑于2021/4/27
            解析字典格式
            """
            obj_dicts = {}
            if isinstance(_obj, dict):
                for key, value in _obj.items():
                    if isinstance(value, list):
                        obj_dicts[key] = parse_list(value)
                    elif isinstance(value, dict):
                        obj_dicts[key] = parse_dict(value)
                    else:
                        v = parse_obj(value)
                        obj_dicts[key] = v
            return obj_dicts

        # 如果他是集合并且里面包含的非字典而是object,则将对象转成字典
        if isinstance(obj, list):
            obj = parse_list(obj)
        elif isinstance(obj, dict):
            obj = parse_dict(obj)
        elif isinstance(obj, object):
            obj = parse_obj(obj)
        # 最后的解析结果
        result = json_to_str(obj)
        if end_load:
            return JsonUtil.load(result)
        elif bf:
            return JsonUtil.beautiful(JsonUtil.load(result))
        return result

    @staticmethod
    def load(item):
        """作者:CACode 最后编辑于2021/4/27
        将json字符串解析成字典
        """
        if isinstance(item, list):
            _dats = []
            for i in item:
                _dats.append(JsonUtil.load(i))
            return _dats
        elif isinstance(item, tuple):
            # 如果是tuple元组则转成集合后递归
            _dats = []
            for i in list(item):
                _dats.append(JsonUtil.load(i))
            return _dats
        elif isinstance(item, dict):
            # 如果是字典,则直接返回
            return item
        elif isinstance(item, str):
            # 如果是字符串则解析为字典
            return JsonUtil.loads(item)
        elif isinstance(item, object):
            # 如果是object则交给parse_obj()解析
            return item.__dict__
        else:
            return JsonUtil.loads(item)

    @staticmethod
    def beautiful(_data):
        """作者:CACode 最后编辑于2021/4/27
        美化json
        """
        return JsonUtil.dumps(_data, sort_keys=True, indent=4, separators=(',', ':'))


class QuerySet(list):
    """
    执行database operation返回的结果集对象

    此序列化器采用链表形式储存数据,递归搜索子节点

    顺序从左子树开始依次按照索引排列

    元类:
        list

    Methods:
        first():
            返回结果集对象的第一个数据

        last():
            返回结果集对象的最后一位参数

        page(size):
            按照每一页有size数量的结果分页

        to_json():
            将结果集对象转json字符串

        add_field():
            添加一个字段使得解析过程中不会被移除

        remove_field():
            删除一个字段使得解析过程中不会添加

        get():
            返回指定位置的参数

    Attribute:

        instance:实例类型模板

        base_data:基本数据

        query_item:使用已有的数据生成QuerySet对象

    """

    def __init__(self, instance=None, base_data=None, query_items=None):
        """
        初始化传入结果集并附加上base_data数据集

        instance:
            序列化的实例对象

        base_data:
            初始化数据源
        """
        list.__init__([])
        if query_items is None:
            self.__instance__ = instance
            # 合并结果集对象
            self.extend(base_data)
        else:
            self.extend(query_items)

    def size(self):
        return len(self)

    def first(self):
        """
        取得结果集的第一位参数
        """
        return self[0]

    def last(self):
        """
        取得结果集的最后一位参数
        """
        return self[len(self) - 1]

    def page(self, size):
        """
        将结果集按照指定数目分割
        """
        return PageHelp.list_of_groups(init_list=self, size=size)

    def to_json(self, bf=False):
        """
        将结果集对象转json处理
        :param bf:是否需要美化sql
        """
        result = []
        for i in self:
            result.append(JsonUtil.load(i.to_json(bf=bf)))
        return JsonUtil.parse(result, bf=bf)

    def to_dict(self):
        return JsonUtil.load(self.to_json())

    def add_field(self, key, default_value=None):
        """
        添加一个不会被解析忽略的字段
        """

        [self[i].add_field(key, default_value) for i in range(len(self))]

    def remove_field(self, key):
        """
        添加一个会被解析忽略的字段
        """
        [self[i].remove_field(key) for i in range(len(self))]

    def get(self, index):
        """
        返回指定位置的元素
        """
        return self[index]

    def __str__(self):
        return self.to_json()

    __repr__ = __str__


#
# class QueryItem(JsonUtil):
#     """
#     序列化器的子节点
#
#     此节点处于二叉树的叶子节点,node分布在各个data_dict
#
#     """
#
#     def __init__(self, ignore_field: dict, append_field: dict, data_item: list, using_fields):
#         # 忽略和添加字段的对象地址值
#         # 调用时从栈钟取出
#         self.ignore_field = ignore_field
#         self.append_field = append_field
#         # 数据初始化的字典
#         self.data_item = data_item
#         self.data_dict = data_item.__dict__
#         # 存在的字段
#         self.using_fields = using_fields
#
#         self.__dict_data__ = {}
#         self.__json_data__ = ""
#
#     def to_json(self, bf=False):
#         """
#         将此叶子节点转json处理
#         """
#         # 从内存地址获取限定对象
#         # 将需要的和不需要的合并
#         if not self.__json_data__:
#             all_fields = dict(self.using_fields, **self.append_field)
#             # 将需要忽略的字典从字典中删除
#             for i in self.ignore_field.keys():
#                 if i in all_fields.keys():
#                     del all_fields[i]
#
#             # 将不存在字段删除
#             for i in all_fields.keys():
#                 if i in self.data_dict.keys():
#                     all_fields[i] = getattr(self.data_item, i)
#
#             self.__json_data__ = self.parse(obj=all_fields, bf=bf)
#
#         return self.__json_data__
#
#     def to_dict(self):
#         """
#         将数据集转字典格式
#         """
#         if not self.__dict_data__:
#             self.__dict_data__ = JsonUtil.load(self.to_json())
#         return self.__dict_data__
#
#     def add_field(self, key, default_value=None):
#         """
#         添加一个不会被解析忽略的字段
#         """
#         if key not in self.append_field.keys() and \
#                 key not in self.using_fields.keys():
#
#             self.append_field[key] = default_value
#         else:
#             CACodeLog.log(obj=self, msg='`{}` already exists'.format(key))
#
#     def remove_field(self, key):
#         """
#         添加一个会被解析忽略的字段
#         """
#         self.ignore_field[key] = None


class PageHelp(list):
    def __init__(self, init_data: list):
        list.__init__([])

        self.__dict_data__ = {}
        self.__json_data__ = ""

        self.extend(init_data)

    def to_dict(self):
        """
        节省资源
        """
        if not self.__dict_data__:
            self.__dict_data__ = JsonUtil.load(self.to_json())
        return self.__dict_data__

    def to_json(self, bf=False):
        """
        节省资源
        """
        if not self.__json_data__:
            json_str = [i.to_dict() for i in self]
            self.__json_data__ = JsonUtil.parse(json_str, bf)
        return self.__json_data__

    @classmethod
    def list_of_groups(cls, init_list, size):
        """
        将数据集按照一定数量分组并返回新数组
        """
        list.__init__([])
        lo_groups = zip(*(iter(init_list),) * size)
        end_list = [QuerySet(query_items=i) for i in lo_groups]
        count = len(init_list) % size
        end_list.append(QuerySet(
            query_items=init_list[-count:])) if count != 0 else QuerySet(query_items=end_list)
        return PageHelp(end_list)

    def get(self, index):
        return self[index]
