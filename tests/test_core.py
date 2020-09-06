import unittest
from enum import Enum

from click.testing import CliRunner

from tests.utils import get_values, get_options
from glacier.core import _get_click_command


class Env(Enum):
    DEV = 'development'
    PROD = 'production'


def my_function_google(
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
        verbose: If set, verbose output will be shown.
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


def my_function_numpy_docstring(
    _path: str,
    name: str,
    age: int,
    is_test: bool,
    env: Env,
    verbose: bool = False,
) -> None:
    """
    This is my test function for generating CLI entrypoint.

    Parameters
    ----------
    _path: str
        path input
    name: str
        Name of the user.
    age: int
        Age of the user.
    is_test: bool
        whether it is test or not.
    env: Env
        Environment where to run the CLI.
    verbose: bool
        If set, verbose output will be shown.
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


def my_function_restructured_text_docstring(
    _path: str,
    name: str,
    age: int,
    is_test: bool,
    env: Env,
    verbose: bool = False,
) -> None:
    """
    This is my test function for generating CLI entrypoint.

    :param _path: path input
    :param name: Name of the user.
    :param age: Age of the user.
    :param is_test: whether it is test or not.
    :param env: Environment where to run the CLI.
    :param verbose: If set, verbose output will be shown.
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
        for function in [
            my_function_google,
            my_function_numpy_docstring,
            my_function_restructured_text_docstring,
        ]:
            f = _get_click_command(function)
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
        for function in [
            my_function_google,
            my_function_numpy_docstring,
            my_function_restructured_text_docstring,
        ]:
            f = _get_click_command(function)
            runner = CliRunner()
            result = runner.invoke(f, [
                '-h',
            ])
            # No exception occurs.
            assert not result.exception
            # Assert that docstring description is contained in help.
            assert (
                'This is my test function for generating CLI entrypoint.'
                in result.output
            )

            # Assert that options are displayed in order.
            help_options = get_options(result.output)

            # Assert the name (and its order) of options
            assert help_options[0].name == 'name'
            assert help_options[1].name == 'age'
            assert help_options[2].name == 'is-test'
            assert help_options[3].name == 'env'
            assert help_options[4].name == 'verbose'

            # Assert that desired description is included in each line
            assert 'Name of the user' in help_options[0].line
            assert 'Age of the user.' in help_options[1].line
            assert 'whether it is test or not.' in help_options[2].line
            assert 'Environment where to run the CLI.' in help_options[3].line
            assert 'If set, verbose output will be shown.' in help_options[4].line
        return
