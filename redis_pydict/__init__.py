from os import stat
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
        return namespace + "&&" +  key
    
    @staticmethod
    def unpack_key(key_string):
        return key_string.split("&&")[1]


class PyRedisDict:

    def __init__(self, host='localhost', port=6379, db=0, password=None, namespace="", custom=None):
        self.redis = custom if custom else redis.Redis(
            host=host, port=port, db=db, password=password
        )

        self.key_namespace = namespace
    
    def _scan_iter(self, pattern):
        formatted_pattern = DataFunctions.define_key(self.key_namespace, pattern)
        return self.redis.scan_iter(formatted_pattern)

    # basic GET and SET functions
    
    def get(self, key, default):
        key = DataFunctions.define_key(self.key_namespace, key)
        data = self.redis.get(key)
        if not data:
            return default
        return DataFunctions.decode(data)
    
    def __setitem__(self, key, value):
        key = DataFunctions.define_key(self.key_namespace, key)
        data = DataFunctions.encode(value)

        self.redis.set(key, data)
    
    def __getitem__(self, key):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        data = self.redis.get(key_formatted)
        if not data:
            raise KeyError(key)
        return DataFunctions.decode(data)
    
    def __delitem__(self, key):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        return_value = self.redis.delete(key_formatted)
        if return_value == 0:
            raise KeyError(key)
    
    def __contains__(self, key):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        return self.redis.exists(key_formatted)
    
    # iteration functions
    
    def _iter_internal(self, pattern):
        scan_iter = self._scan_iter(pattern)
        keys = ( DataFunctions.unpack_key(key) for key in scan_iter )
        return keys
    
    def _iter_items(self, pattern):
        return [
            (key, self[key])
            for key in self._iter_internal(pattern)
        ]
    
    def __iter__(self):
        return self._iter_internal('*')
    
    def items(self):
        return self._iter_items('*')
    
    def iter_matching(self, pattern='*'):
        return self._iter_internal(pattern)
    
    def items_matching(self, pattern='*'):
        return self._iter_items(pattern)

    # mulit-data operations
    def keys(self):
        return self._iter_items('*')
    
    def clear(self):
        keys = list(self._scan_iter('*'))
        self.redis.delete(*keys)
    
    def values(self):
        keys = list(self._scan_iter('*'))
        return [ 
            DataFunctions.decode(value) 
            for value in self.redis.mget(*keys)  
        ]
    
    def update(self, from_dic):
        pipeline = self.redis.pipeline()
        for key, value in from_dic.items():
            formatted_key, encoded_value = DataFunctions.define_key(key), DataFunctions.encode(value)
            pipeline.set(formatted_key, encoded_value)
        pipeline.execute()
    
    def to_dict(self):
        return {
            key: value for key, value in self.items()
        }
    