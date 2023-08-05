# coding: utf-8
from pymongo import MongoClient


class BaseMongoDB(object):
    """
    数据库基类
    """

    def __init__(self, name, host, port, db, **kwargs):
        self.name = name
        # self.client = MongoClient(host, port, **kwargs)
        # self.client.admin.authenticate(config.database.username, config.database.password)
        if 'password' in kwargs and 'user' in kwargs:
            mongo_url = 'mongodb://{0}:{1}@{2}:{3}/?authSource={4}&authMechanism=SCRAM-SHA-1'.format(
                kwargs['user'], kwargs['password'], host, port, db)
        else:
            mongo_url = 'mongodb://{0}:{1}/?authSource={2}&authMechanism=SCRAM-SHA-1'.format(host, port, db)
        # mongo_url = parse.quote(mongo_url)
        self.client = MongoClient(mongo_url)
        self.db = self.client[db]
        self.task = self.db[self.name]

    def change_table(self, name):
        self.name = name
        self.task = self.db[self.name]

    def get_one(self, key: dict):
        return self.task.find_one(key)

    def find(self, key: dict):
        return self.task.find(key)

    def get_all(self):
        return [data for data in self.task.get()]

    def delete_many(self, key: dict):
        return self.task.delete_many(key).deleted_count

    def delete_one(self, key: dict):
        return self.task.delete_one(key).raw_result

    def put(self, obj: dict):
        return self.task.insert_one(obj)

    def update_many(self, key: dict, obj: dict):
        return self.task.update_many(key, {"$set": obj}, upsert=True).raw_result

    def update_one(self, key: dict, obj: dict):
        return self.task.update_one(key, {"$set": obj}, upsert=True).raw_result

    def increment_one(self, key: dict, obj_key: str, step: int):
        """
        对表里的某个数进行自增、自减操作
        [注意]对于嵌套型的数据，需要使用如下格式
        obj_key: "scan_type.s"
        :param key: 索引的key
        :param obj_key:目标的key
        :param step: 增减幅度
        :return:
        """
        return self.task.update_one(key, {"$inc": {obj_key: step}})


"""
由于mongodb中key值不能存在'.'，故对于字典的key值全部进行转换
于是有下面的两个方法
"""


def save_change(d):
    """
    清洗变量d，将其中所有字典key的'.'变为'|'
    """
    if not isinstance(d, dict):
        pass
    else:
        point_to_m(d)
        for key in list(d):
            save_change(d[key])
    return d


def load_change(d):
    """
    清洗变量d，将其中所有字典key的'|'变为'.'
    """
    if not isinstance(d, dict):
        pass
    else:
        m_to_point(d)
        for key in list(d):
            save_change(d[key])
    return d


def point_to_m(t: dict):
    for key in list(t):
        if '.' in key:
            nk = str(key).replace('.', '|')
            t[nk] = t.pop(key)
    return t


def m_to_point(t: dict):
    for key in list(t):
        if '.' in key:
            nk = str(key).replace('|', '.')
            t[nk] = t.pop(key)
    return t


if __name__ == '__main__':
    a = {'a.b': 'c', 'd': 'e', 'fg': {'h': 'i', 'j.k': 'l'}}
    b = save_change(a)
    print(b)
    c = {'d': 'e', 'a|b': 'c', 'f|g': {'h': 'i', 'j|k': 'l'}}
