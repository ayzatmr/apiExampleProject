from enum import Enum


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def list(cls):
        """Returns a list of all the enum values."""
        return sorted(list(cls._value2member_map_.keys()))

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return sorted(cls._member_names_)
