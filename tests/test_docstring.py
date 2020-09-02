import unittest

from glacier.docstring import Arg, Doc, GoogleParser


class TestArg(unittest.TestCase):
    def test_arg_of_lines(self) -> None:
        arg_lines = [
            'hoge: description of hoge',
            '      that can be multilined.',
            'fuga: description of fu-',
            '      ga.',
        ]
        args = Arg.of_lines(arg_lines)
        assert args == [
            Arg(name='hoge', description='description of hoge that can be multilined.'),
            Arg(name='fuga', description='description of fuga.'),
        ]


class TestDocstring(unittest.TestCase):

    # -------------------------------------
    # Google
    # -------------------------------------
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
