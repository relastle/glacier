from glacier import glacier


def run(name: str, verbose: bool = False) -> None:
    """ Run """
    pass


def build(name: str, verbose: bool = False) -> None:
    """ Build """
    pass


def test(name: str, verbose: bool = False) -> None:
    """ Test """
    return


if __name__ == '__main__':
    glacier([run, build, test])
