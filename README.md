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

redis_dict = PyRedisDict(
    host='localhost',     # redis host
    port=6379,            # redis port
    db=0,                 # redis db (0-15)
    password=None,        # password if using password auth
    namespace="",         # namespace: this is the key prefix, every key inserted into the dict will be prefixed with this namespace string when inserting into Redis, this provides some degree of isolation between namespaces
    custom=None  # use a custom connection, pass a Redis/Redis cluster connection object manually, parameters like `host`, `port`, `db` and `password` will be ignored if this is not None
)
```

2. Supported functions:
`PyRedisDict` is a replacement for dict, and it supports most of the dictionary methods:
```
>>> dir(redis_dict)
['__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_iter_internal', '_iter_items', '_scan_iter', 'clear', 'enable_publish', 'get', 'items', 'items_matching', 'iter_matching', 'key_namespace', 'keys', 'notification_id', 'redis', 'set_notification_id', 'set_notification_mode', 'subscribe_to_key_events', 'to_dict', 'update', 'values']
```

3. Publish and subscribe to key set events
`PyRedisDict` can also send key set events when enabled, by default it is not enabled. You can enable it by calling `set_notification_mode(true)` and `set_notification_id(unique_id)`. Every instance of `PyRedisDict` should be set to a unqiue ID to help diffreniciating with each of them. Here is an example

On the sender side:

```python
# enable notifications
redis_dict.set_notification_mode(true)

# set a unique id
redis_dict.set_notification_id('myprocess1')

# now this operation will also publish an event which can be captured by subscribers
redis_dict['key'] = "Hello"
```

On receiver side:
```python
# this will listen for key set events for key 'key' in the given namespace
for (key, notification_id, value) in redis_dict.subscribe_to_key_events(pattern="key"):
    print(key, notification_id, value)

# optionally you can also use a regex pattern, this example listen for all key events matching pattern key*
for (key, notification_id, value) in redis_dict.subscribe_to_key_events(pattern="key*"):
    print(key, notification_id, value)
```

### Examples:
1. Basic set and get
```python
def test_basic_get_set():
   d = PyRedisDict(namespace="mykeyspace")

   d.clear()
   d['none'] = None
   d['int'] = 10
   d['float'] = 20.131
   d['array'] = [10, 20, 30]
   d['hashmap'] = {'name': 'prasanna', 'meta': {'age': 24, 'hobbies': ['gaming']}}

   # assert values
   assert d['int'] == 10
   assert d['float'] == 20.131
   assert d['array'] == [10, 20, 30]
   assert (d['hashmap']['name'] == 'prasanna') and (d['hashmap']['meta']['age'] == 24)
   assert (d['none'] == None)

   d.clear()
```

2. Custom objects
```
def test_custom_class_get_set():
   d = PyRedisDict(namespace="mykeyspace")

   d.clear()
   d['obj'] = CustomClass()

   assert d['obj'].add() == (10 + 20 + 30)
   d.clear()
```
**Note**: `PyRedisDict` uses `cPickle` for custom objects.

3. Iterations
```python
def test_iterations():

   d = PyRedisDict(namespace="mykeyspace2")
   d.clear()
   d['mykey_none'] = None
   d['mykey_int'] = 10
   d['mykey_float'] = 20.131
   d['array'] = [10, 20, 30]
   d['hashmap'] = {'name': 'prasanna', 'meta': {'age': 24, 'hobbies': ['gaming']}}

   # assert values
   assert len(d) == 5
   assert len(d.items()) == 5

   # find by prefix
   assert len(d.items_matching('mykey*')) == 3
   d.clear()
```

4. Key deletion
```python
def test_deletion():

   d = PyRedisDict(namespace="mykeyspace3")

   d.clear()
   d['x1'] = CustomClass()
   d['x2'] = CustomClass()
   d['x3'] = CustomClass()
   d['x4'] = CustomClass()
   d['x4'] = CustomClass()

   assert 'x1' in d
   del d['x1']

   assert 'x1' not in d

   d.clear()
   assert len(d) == 0
```

5. Converting to/from dict
```python
def test_conversions():
   d = PyRedisDict(namespace="mykeyspace")

   d.clear()

   d['mykey_none'] = None
   d['mykey_int'] = 10
   d['mykey_float'] = 20.131
   d['array'] = [10, 20, 30]
   d['hashmap'] = {'name': 'prasanna', 'meta': {'age': 24, 'hobbies': ['gaming']}}

   assert len(d.to_dict()) == 5

   normal_dict = {"mykey_1": 10, "mykey_2": 20, "mykey_3": "hello", "array": [50, 60, 70]}
   d.update(normal_dict)

   assert len(d) == (5 + 3) # another key is duplicate (array)
   assert d['array'] == [50, 60, 70]
   d.clear()
```

### Running tests
This project uses `pytest` for testing. Instal pytest and run `pytest` to validate tests, make sure you set-up Redis locally to test the process.

### Contributions
Feel free to try this library, suggest changes, raise issues, send PRs.