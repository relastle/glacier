from enum import Enum

from glacier import glacier


def main_google(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    Args:
        _path: Positional argument representing the target file path.
        name: Name of this operation.
        verbose: Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return


def main_numpy(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    Parameters
    ----------
    _path: str
        Positional argument representing the target file path.
    name: str
        Name of this operation.
    verbose: bool
        Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return


def main_restructured_text(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    :param _path: Positional argument representing the target file path.
    :param name: Name of this operation.
    :param verbose: Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return


if __name__ == '__main__':
    glacier({
        'google': main_google,
        'numpy': main_numpy,
        'restructured-text': main_restructured_text,
    })
