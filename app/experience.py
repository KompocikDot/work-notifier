from enum import Enum


class Experience(Enum):
    INTERN = 1
    ASSISTANT = 2
    JUNIOR = 3
    MID = 4
    SENIOR = 5
    LEAD = 6
    UNKNOWN = 7

    def __str__(self):
        return self.name

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @classmethod
    def str_to_enum(cls, value: str) -> "Experience":
        roles = {
            ("intern", "praktykant", "stażysta"): cls.INTERN,
            ("junior", "młodszy specjalista"): cls.JUNIOR,
            ("mid", "medium", "regular", "specjalista"): cls.MID,
            ("senior", "starszy specjalista", "ekspert"): cls.SENIOR,
            ("kierownik", "lead", "koordynator", "menedżer"): cls.LEAD,
        }

        role_str = value.lower()
        for role_keys, experience in roles.items():
            if any(role in role_str for role in role_keys):
                return experience
        return cls.UNKNOWN
