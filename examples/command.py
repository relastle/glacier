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
    print(_path)
    print(name)
    print(env)
    print(verbose)
    return


if __name__ == '__main__':
    glacier(main)
