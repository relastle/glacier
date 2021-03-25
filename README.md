![image](https://user-images.githubusercontent.com/6816040/91929753-0fe7bf00-ed1a-11ea-8c95-793e2a20fd07.png)

# glacier

glacier is a python CLI building library for minimalists.

<a href="https://pypi.org/project/glacier/"><img src="https://img.shields.io/pypi/v/glacier?color=395c81"/></a>
<a href="https://pypi.org/project/glacier/"><img src="https://img.shields.io/pypi/pyversions/glacier?color=395c81"/></a>
<a href="https://pypi.org/project/glacier/"><img src="https://img.shields.io/pypi/l/glacier?color=395c81"/></a>

<a href="https://github.com/relastle/glacier/actions?query=workflow%3Apythontests"><img src="https://github.com/relastle/glacier/workflows/pythontests/badge.svg"/></a>
<a href="https://github.com/relastle/glacier/actions?query=workflow%3Apypi-publish"><img src="https://github.com/relastle/glacier/workflows/pypi-publish/badge.svg"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Frelastle%2Fglacier?ref=badge_shield"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Frelastle%2Fglacier.svg?type=shield"/></a>
<a href="https://codecov.io/gh/relastle/glacier"><img src="https://codecov.io/gh/relastle/glacier/branch/master/graph/badge.svg?token=IBCYZODDY3"/></a>

* [glacier](#glacier)
  * [Installation](#installation)
  * [Quick start](#quick-start)
  * [Basic Usage](#basic-usage)
     * [CLI without subcommand](#cli-without-subcommand)
     * [CLI with subcommands](#cli-with-subcommands)
        * [Pass a list of functions](#pass-a-list-of-functions)
        * [Pass a dictionary of functions](#pass-a-dictionary-of-functions)
     * [Async entrypoint support](#async-entrypoint-support)
     * [Positional argument](#positional-argument)
     * [Options](#options)
     * [Default value for optional argument](#default-value-for-optional-argument)
     * [Help with docstring](#help-with-docstring)
        * [Google Style](#google-style)
        * [Numpy Style](#numpy-style)
        * [reStructuredText Style](#restructuredtext-style)
     * [Supported types](#supported-types)
  * [Note](#note)
     * [Philosophy](#apple-philosophy)
     * [Warnings](#construction-warnings)
  * [Related works](#related-works)
  * [<a href="./LICENSE">LICENSE</a>](#license)

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

![quick start help](https://user-images.githubusercontent.com/6816040/92337363-fd87cf80-f0e3-11ea-8902-d0488fbd8547.png)


## Basic Usage

### CLI without subcommand

If you just call `glacier` to a function, it will invoke it as stand-alone CLI
(like the example in [Quick start](https://github.com/relastle/glacier#quick-start)).

### CLI with subcommands

You can easily construct CLI with subcommands in the following two ways.

#### Pass a list of functions

```python
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
```

If you passes a lift of function, glacier constructs the CLI with subcommands whose names are the same as the declared function names.
In this example, the subcommans will be `run`,  `build`, and `test`.


![sub commands help](https://user-images.githubusercontent.com/6816040/92397064-108cb500-f161-11ea-9cb2-0f0a1c4da2f5.png)


#### Pass a dictionary of functions

You can easily give the different name as the subcommand name from any declared name of the function.
Just give a dictionary (key will be a subcommand name).


```python
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
```

This works exactly the same as the previous example.

This interface makes it very easy to build a simple CLI tool from an existing project.

### Async entrypoint support

You sometiems want your async function to be a CLI entrypoint.
Only you have to do is just passing the async function as if it were `sync` function.

The example below combine two async functions and a sync function into CLI
with nested subcommand structure.


```python
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
```

### Positional argument

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
<command_name> <value of a> <value of b> <value of c>
```

### Options

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
<command_name> --a <value of a> --b <value of b> --c <value of c>
```

### Default value for optional argument

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

### Help with docstring

Help message for options or command itself can be provided with python docstring.

Following style of doctrings are supported

- [Google Style](https://github.com/relastle/glacier#google-style)
- [Numpy Style](https://github.com/relastle/glacier#numpy-style)
- [reStructuredText Style](https://github.com/relastle/glacier#restructuredtext-style)

The functions with docstring below will produce the exact the same help message with fed into `glacier`.
(You don't neet to specify which docstring style is used 😄)

#### Google Style

```python
def main_google(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    Args:
        _path: Positional argument representing the target file path.
        name: Name of this operation.
        verbose: Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return
```

#### Numpy Style

```python
def main_numpy(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    Parameters
    ----------
    _path: str
        Positional argument representing the target file path.
    name: str
        Name of this operation.
    verbose: bool
        Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return
```

#### reStructuredText Style


```python
def main_restructured_text(
    _path: str,
    name: str,
    verbose: bool = False,
) -> None:
    """
    This is my simple entry point of CLI.

    :param _path: Positional argument representing the target file path.
    :param name: Name of this operation.
    :param verbose: Verbose output will be shown if set.
    """
    print(_path)
    print(name)
    print(verbose)
    return
```


### Supported types

- [x] int
- [x] str
- [x] bool
- [x] Enum
- [ ] List[int]
- [ ] List[str]

## Note

### :apple: Philosophy

- This library is made for building CLI quickly especially for personal use, so the features provided by it is not rich.

- If you want to build really user-friend CLI or that in production, I suggest that you use [click](https://click.palletsprojects.com/en/7.x/) (actually glacier uses it internally), or other full-stack CLI builing libraries.

### :construction: Warnings

- Please note that any destructive change (backward incompatible) can be done without any announcement.
- This plugin is in a very early stage of development.  Feel free to report problems or submit feature requests in [Issues](https://github.com/relastle/glacier/issues).

## Related works

- [google/python-fire: Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.](https://github.com/google/python-fire)
- [tiangolo/typer: Typer, build great CLIs. Easy to code. Based on Python type hints.](https://github.com/tiangolo/typer)

## [LICENSE](./LICENSE)

MIT
