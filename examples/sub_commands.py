
from glacier import glacier


def run(
    name: str,
    verbose: bool = False,
) -> None:
    """ Run """
    print(name)
    print(verbose)
    return


def build(
    name: str,
    verbose: bool = False,
) -> None:
    """ Build """
    print(name)
    print(verbose)
    return


def test(
    name: str,
    verbose: bool = False,
) -> None:
    """ Test """
    print(name)
    print(verbose)
    return


if __name__ == '__main__':
    glacier([run, build, test])
