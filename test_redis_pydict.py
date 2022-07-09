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
   d['int'] = 10
   d['float'] = 20.131
   d['array'] = [10, 20, 30]
   d['hashmap'] = {'name': 'prasanna', 'meta': {'age': 24, 'hobbies': ['gaming']}}

   # assert values
   assert d['int'] == 10
   assert d['float'] == 20.131
   assert d['array'] == [10, 20, 30]
   assert (d['hashmap']['name'] == 'prasanna') and (d['hashmap']['meta']['age'] == 24)

def test_custom_class_get_set():
   d = PyRedisDict(namespace="mykeyspace")
   d['obj'] = CustomClass()

   assert d['obj'].add() == (10 + 20 + 30)