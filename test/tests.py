from redis_pydict import PyRedisDict


def test_basic_get_set():
   d = PyRedisDict(namespace="mykeyspace")
   d['int'] = 10
   d['float'] = 20.131
   d['array'] = [10, 20, 30]
   d['hashmap'] = {'name': 'prasanna', 'meta': {'age': 24, 'hobbies': ['gaming']}}

   print(d)

   # assert values
   assert d['int'] == 10
   assert d['float'] == 20.131
   assert d['array'] == [10, 20, 30]
   assert (d['hashmap']['name'] == 'prasanna') and (d['hashmap']['meta']['age'] == 24)