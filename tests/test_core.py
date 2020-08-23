import unittest
from enum import Enum

from click.testing import CliRunner

from water.core import _get_click_command


class MyEnum(Enum):
    CHOICE_1 = 'choice_1'
    CHOICE_2 = 'choice_2'


def my_function(
    _path: str,
    name: str,
    age: int,
    is_test: bool,
    choice: MyEnum,
) -> None:
    """
    This is my test function

    Args:
        _path (str): path input
        name (str): Name of the user.
        age (int): Age of the user.
    """
    assert type(_path) == str
    assert type(name) == str
    assert type(age) == int
    assert type(is_test) == bool
    assert isinstance(choice, MyEnum)
    return


class Test(unittest.TestCase):

    def test_water(self) -> None:
        f = _get_click_command(my_function)
        runner = CliRunner()
        result = runner.invoke(f, [
            'path',
            '--name=relastle',
            '--age=10',
            '--is-test',
            '--choice=choice_1',
        ])
        assert not result.exception
        return
