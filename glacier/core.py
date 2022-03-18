import functools
from enum import Enum
from inspect import Parameter, signature
from typing import (Any, Callable, Coroutine, Dict, List, Optional, Type,
                    TypeVar, Union)

import click
import click_completion
from click_help_colors import HelpColorsCommand, HelpColorsGroup

from glacier.docstring import (Doc, GoogleParser, NumpyParser, Parser,
                               RestructuredTextParser)
from glacier.misc import coro

"""
# TODO

- [x] Enum support.
- [ ] Parse python docstring to display help.
"""

T = TypeVar('T')


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


GlacierFunction = Union[
    Callable[..., None],
    Callable[..., Coroutine[Any, Any, Any]],
]


GlacierUnit = Union[
    List[GlacierFunction],
    Dict[str, GlacierFunction],
]


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
    f: Callable[..., Any],
    click_group: Optional[click.Group] = None,
) -> click.BaseCommand:
    f = coro(f)

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
    for param in reversed(list(sig.parameters.values())):
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
    f: Callable[..., T],
    name: str,
) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapped(*args: Any, **kwargs: Any) -> T:
        return f(*args, **kwargs)
    wrapped.__name__ = name
    return wrapped


@click.option(
    '-i',
    '--case-insensitive/--no-case-insensitive',
    help="Case insensitive completion",
)
@click.argument(
    'shell',
    required=False,
    type=click_completion.DocumentedChoice(click_completion.core.shells),
)
def show_completion(shell: str, case_insensitive: bool) -> None:
    """Show the click-completion-command completion code"""
    extra_env = {
        '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'
    } if case_insensitive else {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))


def glacier_group(
    f: Union[
        List[GlacierFunction],
        Dict[str, Union[GlacierFunction, GlacierUnit]],
    ],
    parent_group: Optional[click.Group] = None,
    group_name: Optional[str] = None,
) -> click.Group:
    """
    Make click group
    """
    if parent_group is None:
        group_cls: Any = click  # type: ignore
    else:
        group_cls = parent_group

    def dummy_group() -> None:
        pass

    if group_name:
        dummy_group = rename(dummy_group, group_name)

    group = group_cls.group(  # type: ignore
        cls=HelpColorsGroup,
        context_settings=CONTEXT_SETTINGS,
        **DEFAULT_COLOR_OPTIONS,
    )(dummy_group)

    if isinstance(f, list):
        # List of functions are passed.
        # The declared name of functions are used as subcommand

        for _f in f:
            _get_click_command(coro(_f), group)

    elif isinstance(f, dict):
        # Dictionary of functions with custom subcommand name as key
        for name, _f in f.items():  # type: ignore
            if callable(_f):
                _get_click_command(rename(coro(_f), name), group)
            else:
                glacier_group(
                    _f,  # type: ignore
                    group,
                    name,
                )
    else:
        raise Exception("The arguments of glacier is wrong.")

    if parent_group is None:
        group.command(  # type: ignore
            cls=HelpColorsCommand,
            context_settings=CONTEXT_SETTINGS,
            **DEFAULT_COLOR_OPTIONS,  # type: ignore
        )(show_completion)

    return group  # type: ignore


def glacier(f: Union[
    GlacierFunction,
    List[GlacierFunction],
    Dict[str, Union[GlacierFunction, GlacierUnit]],
]) -> None:
    """
    Main function making function to command line entrypoint
    """

    if callable(f):
        # Only one function is passed.
        entry_point_f = _get_click_command(f)
    else:
        entry_point_f = glacier_group(f)  # type: ignore
    click_completion.init()
    entry_point_f()
