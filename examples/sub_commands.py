
from glacier import glacier


def run(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


def build(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


def test(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


if __name__ == '__main__':
    glacier([run, build, test])
