import pickle
import json

NONE_TYPE_MAGIC = b'PyDictNoneType'

TYPE_MAGIC = {
    ord('n'): "NoneType",
    ord('i'): "int",
    ord('f'): "float",
    ord('s'): "str",
    ord('d'): "dict",
    ord('l'): "list",
    ord('c'): "custom",
}

TYPE_ENCODE_FUNCTIONS = {
    None: lambda _: b'n',
    int: lambda i: b'i' + str(i).encode('utf-8'),
    float: lambda f: b'f' + str(f).encode('utf-8'),
    str: lambda s: b's' + str(s).encode("utf-8"),
    dict: lambda d: b'd' + json.dumps(d).encode('utf-8'),
    list: lambda l: b'l' + json.dumps(l).encode('utf-8'),
    "custom": lambda c: b'c' + pickle.dumps(c)
}

TYPE_DECODE_FUNCTIONS = {
    ord('n'): lambda _: None,
    ord('i'): lambda i: int(i.decode('utf-8')),
    ord('f'): lambda f: float(f.decode('utf-8')),
    ord('s'): lambda s: s.decode('utf-8'),
    ord('d'): lambda d: json.loads(d),
    ord('l'): lambda l: json.loads(l),
    ord('c'): lambda c: pickle.loads(c)
}
