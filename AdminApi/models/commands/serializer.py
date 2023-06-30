import json
from dataclasses import asdict, astuple


class Serializer:

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def to_dict(self):
        return asdict(self)

    def to_tuple(self):
        return astuple(self)


def dataclass_from_dict(meta_class, input_dict):
    try:
        fieldtypes = meta_class.__annotations__
        return meta_class(**{f: dataclass_from_dict(fieldtypes[f], input_dict[f]) for f in input_dict})
    except AttributeError:
        if isinstance(input_dict, (tuple, list)):
            return [dataclass_from_dict(meta_class.__args__[0], f) for f in input_dict]
        return input_dict
