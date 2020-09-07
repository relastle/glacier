![image](https://user-images.githubusercontent.com/6816040/91929753-0fe7bf00-ed1a-11ea-8c95-793e2a20fd07.png)

# glacier

glacier is a python CLI building library for minimalists.

## Installation

```python
pip install glacier
```

## Quick start

You only have to call `glacier` against the entrypoint function.

```python
from glacier import glacier


def main(name: str, verbose: bool = False) -> None:
    pass


if __name__ == '__main__':
    glacier(main)
```

Then, you can see help 🍰.

<img width="430" alt="Screen Shot 2020-09-07 at 8 27 28" src="https://user-images.githubusercontent.com/6816040/92337363-fd87cf80-f0e3-11ea-8902-d0488fbd8547.png">


## Basic Usage

### CLI without subcommand

If you just call `glacier` to a function, it will invoke it as stand-alone CLI (like the example in Quick start).

### CLI with subcommands

You can easily construct CLI with subcommands in the following two ways.

#### Pass a list of functions

```python

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
   glacier([run, build, test])
```

If you passes a lift of function, glacier constructs the CLI with subcommands whose names are the same as the declared function names.
In this example, the subcommans will be `run`,  `build`, and `test`.


<img width="462" alt="Screen Shot 2020-09-07 at 21 56 27" src="https://user-images.githubusercontent.com/6816040/92397064-108cb500-f161-11ea-9cb2-0f0a1c4da2f5.png">


#### Pass a dictionary of functions

You can easily give the different name as the subcommand name from any declared name of the function.
Just give a dictionary (key will be a subcommand name).


```python
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
```

This works exactly the same as the previous example.

This interface makes it very easy to build a simple CLI tool from an existing project.

#### Positional argument

If the name of function argument is underscore-prefiexed, it is understood as positional argument.

```python
from glacier import glacier


def all_positional(_a: str, _b: str, _c: str) -> None:
    print(_a)
    print(_b)
    print(_c)


if __name__ == '__main__':
    glacier(all_positional)
```

The above example is invoked as follows

```bash
<command_name> <vallue of a> <vallue of b> <vallue of c>
```

#### Options

All other (non-underscore-prefixed) arguments are understood as options.

```python
from glacier import glacier


def all_options(a: str, b: str, c: str) -> None:
    print(a)
    print(b)
    print(c)


if __name__ == '__main__':
    glacier(all_options)
```

The above example is invoked as follows

```bash
<command_name> --a <vallue of a> --b <vallue of b> --c <vallue of c>
```

#### Default value for optional argument

If you set the default value for function argument, it also defines the default value for CLI option.


```python
from glacier import glacier


def default(verbose: bool = False) -> None:
    print(verbose)


if __name__ == '__main__':
    glacier(default)
```

The above example is invoked as follows

```bash
<command_name> # Just call without flag (`False` will be printed)
```

or

```bash
<command_name> --verbose # Call with flag (`True` will be printed)
```

#### Supported types

- int
- str
- bool
- Enum

