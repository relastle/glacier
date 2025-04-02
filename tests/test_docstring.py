import unittest

from glacier.docstring import Arg, Doc, GoogleParser, NumpyParser

from glacier.docstring import RestructuredTextParser


class TestArg(unittest.TestCase):
    def test_arg_of_lines_google(self) -> None:
        arg_lines = [
            'hoge: description of hoge',
            '      that can be multilined.',
            'fuga: description of fu-',
            '      ga.',
        ]
        args = Arg.of_lines_google(arg_lines)
        assert args == [
            Arg(name='hoge', description='description of hoge that can be multilined.'),
            Arg(name='fuga', description='description of fuga.'),
        ]

    def test_arg_of_lines_numpy(self) -> None:
        arg_lines = [
            'hoge: str',
            '      description of hoge following type',
            'fuga:',
            '      description of fuga',
        ]
        args = Arg.of_lines_numpy(arg_lines)
        assert args == [
            Arg(name='hoge', description='description of hoge following type'),
            Arg(name='fuga', description='description of fuga'),
        ]

    def test_arg_of_lines_resttxt(self) -> None:
        arg_lines = [
            ':param hoge: description of hoge.',
            ':param fuga: description of fuga',
            '             multilined.',
        ]
        args = Arg.of_lines_resttxt(arg_lines)
        assert args == [
            Arg(name='hoge', description='description of hoge.'),
            Arg(name='fuga', description='description of fuga multilined.'),
        ]


class TestDocstringGoogle(unittest.TestCase):
    def test_google_one_line_description(self) -> None:
        docstring = """ This is oneline docstring. """
        parser = GoogleParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is oneline docstring.',
            args=[],
        )
        return

    def test_google_simple(self) -> None:
        docstring = """
        This is a simple docstring.

        Args:
            foo: Description of foo.
            bar: Description of bar.
        """
        parser = GoogleParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is a simple docstring.',
            args=[
                Arg(name='foo', description='Description of foo.'),
                Arg(name='bar', description='Description of bar.'),
            ],
        )
        return


class TestDocstringNumpy(unittest.TestCase):
    def test_numpy_one_line_description(self) -> None:
        docstring = """ This is oneline docstring. """
        parser = NumpyParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is oneline docstring.',
            args=[],
        )
        return

    def test_numpy_simple(self) -> None:
        docstring = """
        This is a simple docstring.

        Parameters
        ----------
        foo: str
             Description of foo.
        bar: int
             Description of bar.
        """
        parser = NumpyParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is a simple docstring.',
            args=[
                Arg(name='foo', description='Description of foo.'),
                Arg(name='bar', description='Description of bar.'),
            ],
        )
        return


class TestDocstringRestructuredText(unittest.TestCase):
    def test_resttext_one_line_description(self) -> None:
        docstring = """ This is oneline docstring. """
        parser = NumpyParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is oneline docstring.',
            args=[],
        )
        return

    def test_resttext_simple(self) -> None:
        docstring = """
        This is a simple docstring.

        :param foo: Description of foo.
        :param bar: Description of bar
                    that is multilined.
        """
        parser = RestructuredTextParser()
        doc = parser.parse(docstring)
        assert doc == Doc(
            description='This is a simple docstring.',
            args=[
                Arg(name='foo', description='Description of foo.'),
                Arg(name='bar', description='Description of bar that is multilined.'),
            ],
        )
        return
