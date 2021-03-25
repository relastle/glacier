from glacier import glacier


async def main() -> None:
    return


def sub_1() -> None:
    return


async def sub_2() -> None:
    return


if __name__ == '__main__':
    glacier({
        'main': main,
        'sub': [
            sub_1,
            sub_2,
        ],
    })
