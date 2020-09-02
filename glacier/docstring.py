"""
Parser of docstring
"""
from __future__ import annotations

import re
from typing import List
from dataclasses import dataclass

from typing_extensions import Protocol

ARG_START_PATTERN = re.compile(r'^(\w+): ')


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
    def of_lines(cls, lines: List[str]) -> List[Arg]:
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
            m = re.search(ARG_START_PATTERN, line.lstrip())
            if m:
                if arg_name:
                    args.append(Arg(
                        name=arg_name,
                        description=arg_description_builder.build(),
                    ))
                    arg_description_builder = DescriptionBuilder()
                arg_name = m.group(1)
                arg_description_builder.add_line(re.sub(
                    ARG_START_PATTERN,
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
        return Doc(description_builder.build(), Arg.of_lines(args_lines))


class NumpyParser:
    def parse(self, docstring: str) -> Doc:
        return Doc('', [])
