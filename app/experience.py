from enum import IntEnum


class Experience(IntEnum):
    INTERN = 1
    ASSISTANT = 2
    JUNIOR = 3
    MID = 4
    SENIOR = 5
    LEAD = 6
    UNKNOWN = 7

    def __str__(self):
        return self.name

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
