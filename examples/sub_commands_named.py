
from glacier import glacier


def f1(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


def f2(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


def f3(
    name: str,
    verbose: bool = False,
) -> None:
    print(name)
    print(verbose)
    return


if __name__ == '__main__':
    glacier(
        {
            'run': f1,
            'build': f2,
            'test': f3,
        },
    )
