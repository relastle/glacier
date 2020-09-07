from glacier import glacier


def default(verbose: bool = False) -> None:
    print(verbose)


if __name__ == '__main__':
    glacier(default)
