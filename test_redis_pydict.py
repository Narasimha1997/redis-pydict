from redis_pydict import PyRedisDict


class CustomClass:

   def __init__(self) -> None:
       self.x = 10
       self.y = 20
       self.z = 30
      
   def add(self):
      return self.x + self.y + self.z


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

def test_custom_class_get_set():
   d = PyRedisDict(namespace="mykeyspace")

   d.clear()
   d['obj'] = CustomClass()

   assert d['obj'].add() == (10 + 20 + 30)
   d.clear()

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