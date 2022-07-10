# redis-pydict
A python dictionary that uses Redis as in-memory storage backend to facilitate distributed computing applications development. This library is a small wrapper around Redis that provides dictionary that acts as a drop-in replacement for python dict, but stores data in Redis instead of local program memor, thus key-value pairs written into the python dictionary can be used by other programs that are connected to the same Redis instance / cluster anywhere over the network. The library also provides wrapper around Redis Pub-Sub using which processes can publish and wait for events when new keys are added to the dictionary.

### Installation
1. From source:
```
git clone git@github.com:Narasimha1997/redis-pydict.git
cd redis-pydict
pip3 install -e .
```

2. From PIP
```
pip3 install redis-pydict
```

### Usage
1. Creating the instance of RedisPyDict
```python
from redis_pydict import PyRedisDict

redis_dict = RedisPyDict(
    host='localhost',     # redis host
    port=6379,            # redis port
    db=0,                 # redis db (0-15)
    password=None,        # password if using password auth
    namespace="",         # namespace: this is the key prefix, every key inserted into the dict will be prefixed with this namespace string when inserting into Redis, this provides some degree of isolation between namespaces
    custom=None  # use a custom connection, pass a Redis/Redis cluster connection object manually, parameters like `host`, `port`, `db` and `password` will be ignored if this is not None
)
```

2. Supported functions:



