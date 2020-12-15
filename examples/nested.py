
from glacier import glacier


def main() -> None:
    return


def sub_1() -> None:
    return


def sub_2() -> None:
    return


if __name__ == '__main__':
    glacier({
        'main': main,
        'sub': [
            sub_1,
            sub_2,
        ],
    })
