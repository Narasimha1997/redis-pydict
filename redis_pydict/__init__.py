from os import stat
from turtle import st
from types import NoneType
import pickle
import json
import redis

NONE_TYPE_MAGIC = b'PyDictNoneType'

TYPE_MAGIC = {
    b'n': "NoneType",
    b'i': "int",
    b'f': "float",
    b's': "str",
    b'd': "dict",
    b'l': "list",
    b'c': "custom",
}

TYPE_ENCODE_FUNCTIONS = {
    None: lambda _: b'n',
    int: lambda i: b'i' + str(i).encode('utf-8'),
    float: lambda f: b'f' + str(f).encode('utf-8'),
    str: lambda s: b's' + str(s).encode("utf-8"),
    dict: lambda d: b'd' + json.dumps(d),
    list: lambda l: b'l' + json.dumps(l),
    "custom": lambda c: b'c' + pickle.dumps(c)
}

TYPE_DECODE_FUNCTIONS = {
    "NoneType": lambda _: None,
    "int": lambda i: int(i.decode('utf-8')),
    "float": lambda f: float(f.decode('utf-8')),
    "str": lambda s: s.deocde('utf-8'),
    "dict": lambda d: json.loads(d),
    "list": lambda l: json.loads(l),
    "custom": lambda c: pickle.loads(c)
}

class DataFunctions:

    @staticmethod
    def encode(data):
        type_ = type(data)
        if type_ not in TYPE_ENCODE_FUNCTIONS:
            return TYPE_ENCODE_FUNCTIONS["custom"](data)
        return TYPE_ENCODE_FUNCTIONS[type_](data)
    
    @staticmethod
    def decode(data):
        type_magic = data[0]
        rest_of_data = data[1:]
        return TYPE_DECODE_FUNCTIONS[type_magic](rest_of_data)
    
    @staticmethod
    def define_key(namespace, key):
        return namespace + "(??)" +  key


class PyRedisDict:

    def __init__(self, host='localhost', port=6379, db=0, password=None, namespace="", custom=None):
        self.redis = custom if custom else redis.Redis(
            host=host, port=port, db=db, password=password
        )

        self.key_namespace = namespace

