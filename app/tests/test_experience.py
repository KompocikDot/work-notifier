from unittest import TestCase

from parameterized import parameterized

from app.experience import Experience


class TestWorkifier(TestCase):
    @parameterized.expand(
        [
            ("Junior", Experience.JUNIOR),
            ("miD", Experience.MID),
            ("seNIor", Experience.SENIOR),
            ("koordynator", Experience.LEAD),
            ("", Experience.UNKNOWN),
        ]
    )
    def test_str_to_enum(self, value, expected):
        assert Experience.str_to_enum(value) == expected

    @parameterized.expand(
        [
            (Experience.UNKNOWN, Experience.LEAD),
            (Experience.LEAD, Experience.SENIOR),
            (Experience.SENIOR, Experience.MID),
            (Experience.MID, Experience.JUNIOR),
            (Experience.JUNIOR, Experience.ASSISTANT),
            (Experience.ASSISTANT, Experience.INTERN),
        ]
    )
    def test_experience_differences(self, left, right):
        assert left > right
