from glacier import glacier


def f1(name: str, verbose: bool = False) -> None:
    pass


def f2(name: str, verbose: bool = False) -> None:
    pass


def f3(name: str, verbose: bool = False) -> None:
    pass


if __name__ == '__main__':
    glacier({
        'run': f1,
        'build': f2,
        'test': f3,
    })
