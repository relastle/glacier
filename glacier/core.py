import functools
from enum import Enum
from typing import Any, Dict, List, Type, Union, Callable, Optional
from inspect import Parameter, signature

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from glacier.docstring import (
    Doc,
    Parser,
    NumpyParser,
    GoogleParser,
    RestructuredTextParser
)

"""
# TODO

- [x] Enum support.
- [ ] Parse python docstring to display help.
"""

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


def get_enum_map(f: Callable[..., None]) -> Dict[str, Dict[str, Any]]:
    sig = signature(f)

    # pick enum from signature
    enum_map: Dict[str, Dict[str, Any]] = {}
    for param in sig.parameters.values():
        if issubclass(param.annotation, Enum):
            enum_class = param.annotation
            enum_map.setdefault(param.name, {})
            for enum_entry in enum_class:
                enum_map[param.name][enum_entry.value] = enum_entry
    return enum_map


def glacier_wrap(
    f: Callable[..., None],
    enum_map: Dict[str, Dict[str, Any]],
) -> Callable[..., None]:
    """
    Return the new function which is click-compatible
    (has no enum signature arguments) from the arbitrary glacier compatible
    function
    """

    # Implemented the argument convert logic
    @functools.wraps(f)
    def wrapped(*args: Any, **kwargs: Any) -> None:
        # convert args and kwargs
        converted_kwargs = {}
        for name, value in kwargs.items():
            if name in enum_map:
                converted_kwargs[name] = enum_map[name][value]
            else:
                converted_kwargs[name] = value

        return f(*args, **converted_kwargs)

    return wrapped


def _get_best_doc(docstring: str, arg_names: List[str]) -> Doc:
    """
    Detect the format of docstring and return best help generated from docstring.
    """
    parser_types: List[Type[Parser]] = [
        GoogleParser,
        NumpyParser,
        RestructuredTextParser,
    ]
    docs = [
        parser_type().parse(docstring=docstring)
        for parser_type in parser_types
    ]
    return max(docs, key=lambda doc: doc.get_matched_arg_count(arg_names))


def _get_click_command(
    f: Callable[..., None],
    click_group: Optional[click.Group] = None,
) -> click.BaseCommand:
    # Get signature
    sig = signature(f)

    # Get docstring
    docstring = f.__doc__
    if docstring:
        doc = _get_best_doc(
            docstring=docstring,
            arg_names=[param.name for param in sig.parameters.values()],
        )
        f.__doc__ = doc.description
        arg_help_d = {
            arg.name: arg.description
            for arg in doc.args
        }
    else:
        arg_help_d = {}

    # Precauclate Enum mappings
    enum_map = get_enum_map(f)

    # Return new function which interprets custom type such as Enum.
    click_f: Any = glacier_wrap(f, enum_map)

    # Decorate the function reversely.
    for param in reversed(sig.parameters.values()):
        if param.name.startswith('_'):
            # Positional argument
            click_f = click.argument(
                param.name,
                type=param.annotation,
                nargs=1,
            )(click_f)
        else:
            # Optional argument
            if param.default == Parameter.empty:
                common_kwargs = dict(
                    required=True,
                    help=arg_help_d.get(param.name, ''),
                )
            else:
                common_kwargs = dict(
                    default=param.default,
                    help=arg_help_d.get(param.name, ''),
                )
            if param.annotation == bool:
                # Boolean flag
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    is_flag=True,
                    type=bool,
                    **common_kwargs,
                )(click_f)
            elif param.annotation == str or param.annotation == int:
                # string or boolean option
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    type=param.annotation,
                    **common_kwargs,
                )(click_f)
            elif issubclass(param.annotation, Enum):
                click_f = click.option(  # type: ignore
                    '--' + param.name.replace('_', '-'),
                    type=click.Choice(enum_map[param.name].keys()),
                    **common_kwargs,
                )(click_f)

    if click_group:
        return click_group.command(  # type: ignore
            cls=HelpColorsCommand,
            context_settings=CONTEXT_SETTINGS,
            **DEFAULT_COLOR_OPTIONS,  # type: ignore
        )(click_f)
    else:
        return click.command(  # type: ignore
            cls=HelpColorsCommand,
            context_settings=CONTEXT_SETTINGS,
            **DEFAULT_COLOR_OPTIONS,  # type: ignore
        )(click_f)


def rename(
    f: Callable[..., None],
    name: str,
) -> Callable[..., None]:
    @functools.wraps(f)
    def wrapped(*args: Any, **kwargs: Any) -> None:
        return f(*args, **kwargs)
    wrapped.__name__ = name
    return wrapped


def glacier(f: Union[
    Callable[..., None],
    List[Callable[..., None]],
    Dict[str, Callable[..., None]],
]) -> None:
    """
    Main function making function to command line entrypoint
    """
    if callable(f):
        # Only one function is passed.
        _get_click_command(f)()
    elif isinstance(f, List):
        # List of functions are passed.
        # The declared name of functions are used as subcommand
        @click.group(
            cls=HelpColorsGroup,
            context_settings=CONTEXT_SETTINGS,
            **DEFAULT_COLOR_OPTIONS,  # type: ignore
        )
        def dummy_group() -> None:
            pass

        for _f in f:
            _get_click_command(_f, dummy_group)
        dummy_group()
    elif isinstance(f, Dict):
        # Dictionary of functions with custom subcommand name as key
        @click.group(
            cls=HelpColorsGroup,
            context_settings=CONTEXT_SETTINGS,
            **DEFAULT_COLOR_OPTIONS,  # type: ignore
        )
        def dummy_group() -> None:
            pass

        for name, _f in f.items():
            _get_click_command(rename(_f, name), dummy_group)
        dummy_group()
