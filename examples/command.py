from enum import Enum

from glacier import glacier


class Env(Enum):
    DEV = 'development'
    PROD = 'production'


def main(
    _path: str,
    name: str,
    env: Env,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    Args:
        _path: Positional argument representing the target file path.
        name: Name of this operation.
        env: Specifying this operation is for whether dev or prod.
        verbose: Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(env)
    print(verbose)
    return


if __name__ == '__main__':
    glacier(main)
