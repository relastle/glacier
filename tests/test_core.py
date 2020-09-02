import unittest
from enum import Enum

from click.testing import CliRunner

from tests.utils import get_values, get_options
from glacier.core import _get_click_command


class Env(Enum):
    DEV = 'development'
    PROD = 'production'


def my_function(
    _path: str,
    name: str,
    age: int,
    is_test: bool,
    env: Env,
    verbose: bool = False,
) -> None:
    """
    This is my test function for generating CLI entrypoint.

    Args:
        _path: path input
        name: Name of the user.
        age: Age of the user.
        is_test: whether it is test or not.
        env: Environment where to run the CLI.
    """
    # Check if all arguments have the propery type.
    assert type(_path) == str
    assert type(name) == str
    assert type(age) == int
    assert type(is_test) == bool
    assert isinstance(env, Env)
    assert type(verbose) == bool

    # Print all values
    print(f'_path={_path}')
    print(f'name={name}')
    print(f'age={age}')
    print(f'is_test={is_test}')
    print(f'env={env}')
    print(f'verbose={verbose}')
    return


class TestCore(unittest.TestCase):

    def test_glacier_ok(self) -> None:
        """
        Appropriate pattern (perfectly happy path).
        """
        f = _get_click_command(my_function)
        runner = CliRunner()

        # All required arguments are provided, and
        # verbose (default value is set) is omitted.
        result = runner.invoke(f, [
            'path',
            '--name=taro',
            '--age=10',
            '--is-test',
            '--env=development',
        ])
        # No excption occurs
        assert not result.exception

        # Get output
        res_d = get_values(result.output)
        assert res_d['_path'] == 'path'
        assert res_d['name'] == 'taro'
        assert res_d['age'] == '10'
        assert res_d['is_test'] == 'True'
        assert res_d['env'] == 'Env.DEV'
        assert res_d['verbose'] == 'False'
        return

    def test_glacier_help(self) -> None:
        """
        Check if help of CLI is correct.
        """
        f = _get_click_command(my_function)
        runner = CliRunner()
        result = runner.invoke(f, [
            '-h',
        ])
        # No exception occurs.
        assert not result.exception

        # Assert that docstring description is contained in help.
        assert (
            'This is my test function for generating CLI entrypoint.' in result.output
        )

        # Assert that options are displayed in order.
        options_names = get_options(result.output)
        assert options_names[0] == 'name'
        assert options_names[1] == 'age'
        assert options_names[2] == 'is-test'
        assert options_names[3] == 'env'
        assert options_names[4] == 'verbose'
        return
