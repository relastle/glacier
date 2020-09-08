"""
Parser of docstring
"""
import re
from enum import Enum, auto
from typing import List
from dataclasses import dataclass

from typing_extensions import Protocol

GOOGLE_ARG_START_PATTERN = re.compile(r'^(\w+): ')
NUMPY_ARG_START_PATTERN = re.compile(r'^(\w+):')
RESTTXT_ARG_START_PATTERN = re.compile(r'^:param (\w+):')


@dataclass(init=False)
class DescriptionBuilder:

    last_is_line_break: bool
    description: str

    def __init__(self) -> None:
        self.last_is_line_break = True
        self.description = ''
        pass

    def add_line(self, line: str) -> None:
        if not line:
            if not self.description:
                return
            self.description += '\n'
            self.last_is_line_break = True
            return

        if self.last_is_line_break:
            self.description += line.strip()
        else:
            if self.description.endswith('-'):
                self.description = self.description[:-1] + line.strip()
            else:
                self.description += ' ' + line.strip()
        self.last_is_line_break = False

    def build(self) -> str:
        return self.description.strip()


@dataclass(frozen=True)
class Arg:
    name: str
    description: str

    @classmethod
    def of_lines_google(cls, lines: List[str]) -> List['Arg']:
        """
        Parse the lines of args as following and return the list.

        hoge: description of hoge
              that can be multilined.
        fuga: description of fuga.
        """
        args = []
        arg_name = ''
        arg_description_builder = DescriptionBuilder()
        for line in lines:
            m = re.search(GOOGLE_ARG_START_PATTERN, line.lstrip())
            if m:
                if arg_name:
                    args.append(Arg(
                        name=arg_name,
                        description=arg_description_builder.build(),
                    ))
                    arg_description_builder = DescriptionBuilder()
                arg_name = m.group(1)
                arg_description_builder.add_line(re.sub(
                    GOOGLE_ARG_START_PATTERN,
                    '',
                    line.lstrip(),
                ).strip())
            else:
                arg_description_builder.add_line(line.strip())

        if arg_name:
            args.append(Arg(
                name=arg_name,
                description=arg_description_builder.build(),
            ))
        return args

    @classmethod
    def of_lines_numpy(cls, lines: List[str]) -> List['Arg']:
        """
        Parse the lines of numpy args format as following and return the list.

        hoge: str
            description of hoge
        fuga:
            description of fuga.
        """
        args = []
        arg_name = ''
        arg_description_builder = DescriptionBuilder()
        for line in lines:
            m = re.search(NUMPY_ARG_START_PATTERN, line.lstrip())
            if m:
                if arg_name:
                    args.append(Arg(
                        name=arg_name,
                        description=arg_description_builder.build(),
                    ))
                    arg_description_builder = DescriptionBuilder()
                arg_name = m.group(1)
            else:
                arg_description_builder.add_line(line.strip())

        if arg_name:
            args.append(Arg(
                name=arg_name,
                description=arg_description_builder.build(),
            ))
        return args

    @classmethod
    def of_lines_resttxt(cls, lines: List[str]) -> List['Arg']:
        """
        Parse the lines of reStructuredText args format as following
        and return the list.

        :param hoge: description of hoge
        :param fuga: description of fuga
        """
        args = []
        arg_name = ''
        arg_description_builder = DescriptionBuilder()
        for line in lines:
            m = re.search(RESTTXT_ARG_START_PATTERN, line.lstrip())
            if m:
                if arg_name:
                    args.append(Arg(
                        name=arg_name,
                        description=arg_description_builder.build(),
                    ))
                    arg_description_builder = DescriptionBuilder()
                arg_name = m.group(1)
                arg_description_builder.add_line(re.sub(
                    RESTTXT_ARG_START_PATTERN,
                    '',
                    line.lstrip(),
                ).strip())
            else:
                arg_description_builder.add_line(line.strip())

        if arg_name:
            args.append(Arg(
                name=arg_name,
                description=arg_description_builder.build(),
            ))
        return args


@dataclass(frozen=True)
class Doc:
    description: str
    args: List[Arg]

    def get_matched_arg_count(self, real_args: List[str]) -> int:
        """ Get the number of given argument names which is also
        in docstring.
        """

        return sum([
            (arg.name in real_args) for arg in self.args
        ])


class Parser(Protocol):
    def parse(self, docstring: str) -> Doc:
        pass


class GoogleParser:
    def parse(self, docstring: str) -> Doc:
        docstring_lines = docstring.splitlines()
        description_builder = DescriptionBuilder()
        found_args_indicator = False
        ends_args_section = False
        args_lines = []
        for i, line in enumerate(docstring_lines):
            if line.strip() == 'Args:':
                found_args_indicator = True
                continue

            if not found_args_indicator:
                description_builder.add_line(line)
            elif not line.strip():
                ends_args_section = True
            elif not ends_args_section:
                args_lines.append(line)
        return Doc(description_builder.build(), Arg.of_lines_google(args_lines))


class NumpyParserState(Enum):
    IN_DESCRIPTION = auto()
    FOUND_PARAMETERS = auto()
    FOUND_PARAMETERS_LINE = auto()


class NumpyParser:

    def parse(self, docstring: str) -> Doc:
        docstring_lines = docstring.splitlines()
        description_builder = DescriptionBuilder()
        state: NumpyParserState = NumpyParserState.IN_DESCRIPTION
        args_lines = []
        for i, line in enumerate(docstring_lines):
            if state == NumpyParserState.IN_DESCRIPTION:
                if line.strip() == 'Parameters':
                    state = NumpyParserState.FOUND_PARAMETERS
                    continue
                description_builder.add_line(line)
            elif state == NumpyParserState.FOUND_PARAMETERS:
                if line.strip() == '----------':
                    state = NumpyParserState.FOUND_PARAMETERS_LINE
                    continue
            elif state == NumpyParserState.FOUND_PARAMETERS_LINE:
                args_lines.append(line)
        return Doc(description_builder.build(), Arg.of_lines_numpy(args_lines))


RESTTXT_ITEM_PATTERN = re.compile(r'^:(\w+) (\w+):')


class RestructuredTextParser:

    def parse(self, docstring: str) -> Doc:
        docstring_lines = docstring.splitlines()
        description_builder = DescriptionBuilder()
        started_args = False
        args_lines = []
        for i, line in enumerate(docstring_lines):
            m = re.search(RESTTXT_ITEM_PATTERN, line.lstrip())
            if m:
                item_name = m.group(1)
                if item_name == 'param':
                    started_args = True
                    args_lines.append(line)
                else:
                    break
            elif started_args:
                args_lines.append(line)
            else:
                description_builder.add_line(line)

        return Doc(description_builder.build(), Arg.of_lines_resttxt(args_lines))
