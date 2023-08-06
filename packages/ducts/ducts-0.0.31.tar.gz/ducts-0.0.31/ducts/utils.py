import types

def nameddict(name, dict_keys: str):
    keys = []
    if isinstance(dict_keys, str):
        keys = [v for v in dict_keys.split(' ') if v]
    elif isinstance(dict_keys, (list, tuple)):
        keys = [v for v in [val.strip() for val in dict_keys] if v]
    else:
        ValueError('dict_keys must be str or list but was [{}]'.format(type(dict_keys)))
    
    def create_property(attr):
        def getter(self):
            try:
                return self[attr]
            except KeyError:
                return None

        def setter(self, value):
            self[attr] = value
        return property(getter, setter)
        
    def init(self, dict={}):
        NamedDict.__init__(self, dict)
    
    def setattribute(self, attr, val):
        if not hasattr(self, attr):
            raise AttributeError("'{}' object has no attribute '{}'".format(name, attr))
        NamedDict.__setattr__(self, attr, val)

    def update_ns(ns):
        for attr in keys:
            ns[attr] = create_property(attr)
        ns['KEYS'] = keys
        ns['__init__'] = init
        ns['__setattr__'] = setattribute

    return types.new_class(name, bases=(NamedDict,), exec_body=update_ns)
    

class NamedDict(dict):

    def __init__(self, dict = None):
        super().__init__(dict)

    def __str__(self):
        return '{}[{}]'.format(self.__class__.__name__, super().__str__())

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def copy(self):
        return self.__class__(super().copy())

