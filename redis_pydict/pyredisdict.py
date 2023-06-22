from typing import *
import redis
from .const import NONE_TYPE_MAGIC,\
    TYPE_MAGIC,\
    TYPE_ENCODE_FUNCTIONS,\
    TYPE_DECODE_FUNCTIONS


class DataFunctions:

    @staticmethod
    def encode(data: Any):
        type_ = type(data)
        if type_ not in TYPE_ENCODE_FUNCTIONS:
            return TYPE_ENCODE_FUNCTIONS["custom"](data)
        return TYPE_ENCODE_FUNCTIONS[type_](data)

    @staticmethod
    def decode(data: bytes):
        type_magic = data[0]

        rest_of_data = data[1:]
        return TYPE_DECODE_FUNCTIONS[type_magic](rest_of_data)

    @staticmethod
    def define_key(namespace: str, key: Any):
        return namespace + "&&" + str(key)

    @staticmethod
    def unpack_key(key: bytes):
        key_string = key.decode('utf-8')
        return '&&'.join(key_string.split("&&")[1:])


class PyRedisDict:

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0,
                 password: str = None,
                 namespace: str = "",
                 custom: Any = None):
        self.redis = custom if custom else redis.Redis(
            host=host, port=port, db=db, password=password)

        self.key_namespace = namespace
        self.enable_publish = False
        self.notification_id = ""

    def set_notification_mode(self, enable: bool):
        self.enable_publish = enable

    def set_notification_id(self, note_id: str):
        self.notification_id = note_id

    def _scan_iter(self, pattern: Any):
        formatted_pattern = DataFunctions.define_key(self.key_namespace,
                                                     pattern)
        return self.redis.scan_iter(formatted_pattern)

    # basic GET and SET functions

    def get(self, key: Any, default: Any):
        key = DataFunctions.define_key(self.key_namespace, key)
        data = self.redis.get(key)
        if not data:
            return default
        return DataFunctions.decode(data)

    def __setitem__(self, key: Any, value: Any):
        key = DataFunctions.define_key(self.key_namespace, key)
        data = DataFunctions.encode(value)
        self.redis.set(key, data)

        # push notification if enabled
        if self.enable_publish:
            self.redis.publish("event_" + key, self.notification_id)

    def __getitem__(self, key: Any):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        data = self.redis.get(key_formatted)
        # print(data)
        if not data:
            raise KeyError(key)
        return DataFunctions.decode(data)

    def __delitem__(self, key: Any):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        return_value = self.redis.delete(key_formatted)
        if return_value == 0:
            raise KeyError(key)

    def __contains__(self, key: Any):
        key_formatted = DataFunctions.define_key(self.key_namespace, key)
        return self.redis.exists(key_formatted)

    # iteration functions

    def _iter_internal(self, pattern: Any):
        scan_iter = self._scan_iter(pattern)
        keys = (DataFunctions.unpack_key(key) for key in scan_iter)
        return keys

    def _iter_items(self, pattern: Any):
        return [(key, self[key]) for key in self._iter_internal(pattern)]

    def __iter__(self):
        return self._iter_internal('*')

    def items(self):
        return self._iter_items('*')

    def iter_matching(self, pattern: Any = '*'):
        return self._iter_internal(pattern)

    def items_matching(self, pattern: Any = '*'):
        return self._iter_items(pattern)

    # mulit-data operations
    def keys(self):
        return self._iter_items('*')

    def clear(self):
        keys = list(self._scan_iter('*'))
        if len(keys) != 0:
            self.redis.delete(*keys)

    def values(self):
        keys = list(self._scan_iter('*'))
        return [
            DataFunctions.decode(value) for value in self.redis.mget(*keys)
        ]

    def update(self, from_dic: Any):
        pipeline = self.redis.pipeline()
        for key, value in from_dic.items():
            formatted_key, encoded_value = DataFunctions.define_key(
                self.key_namespace, key), DataFunctions.encode(value)
            pipeline.set(formatted_key, encoded_value)
        pipeline.execute()

    def to_dict(self):
        return {key: value for key, value in self.items()}

    def __len__(self):
        return len(list(self._scan_iter('*')))

    def __str__(self) -> str:
        return str(self.to_dict())

    def subscribe_to_key_events(self, pattern: Any = "*"):
        channel_name = DataFunctions.define_key("event_" + self.key_namespace,
                                                pattern)
        pusub = self.redis.pubsub()
        pusub.subscribe(channel_name)

        for message in pusub.listen():
            if message and type(
                    message) == dict and message['type'] == 'message':
                notification_id = message['data'].decode('utf-8')
                channel_complete_name = message['channel'].decode('utf-8')
                if not channel_complete_name.startswith('event_'):
                    pass

                channel = channel_complete_name[6:]
                channel = '&&'.join(channel.split('&&')[1:])
                value = self[channel]

                yield (channel, notification_id, value)
