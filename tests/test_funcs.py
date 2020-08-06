import types

from password_validation.funcs import FormatXY
from password_validation.funcs import greater_than_or_equal_to
from password_validation.funcs import less_than_or_equal_to
from password_validation.funcs import not_in
from password_validation.funcs import statement


def test_format_xy():
    some_text = "x and y"
    format_text = FormatXY(some_text)
    assert format_text
    assert isinstance(format_text, FormatXY)

    formatted_text = format_text(x="hello", y="world")
    assert formatted_text == '"hello" and "world"'


def test_statement():
    def f():
        return

    f = statement("hello world")(f)

    assert f.statement == "hello world"
    assert f.format_statement(x="hello", y="world") == f.statement

    @statement("hello x and y")
    def g():
        return

    assert g.statement == "hello x and y"
    assert g.format_statement(x="goodbye", y="yo") == 'hello "goodbye" and "yo"'


def test_greater_than_or_equal_to():
    assert greater_than_or_equal_to(1, 2) is False
    assert greater_than_or_equal_to(1, 1) is True
    assert greater_than_or_equal_to(2, 1) is True

    assert greater_than_or_equal_to.statement == "x >= y"

    assert eval(
        greater_than_or_equal_to.format_statement(x=1, y=2)
    ) == greater_than_or_equal_to(1, 2)
    assert eval(
        greater_than_or_equal_to.format_statement(x=1, y=1)
    ) == greater_than_or_equal_to(1, 1)
    assert eval(
        greater_than_or_equal_to.format_statement(x=2, y=1)
    ) == greater_than_or_equal_to(2, 1)


def test_less_than_or_equal_to():
    assert less_than_or_equal_to(1, 2) is True
    assert less_than_or_equal_to(1, 1) is True
    assert less_than_or_equal_to(2, 1) is False

    assert less_than_or_equal_to.statement == "x <= y"

    assert eval(
        less_than_or_equal_to.format_statement(x=1, y=2)
    ) == less_than_or_equal_to(1, 2)
    assert eval(
        less_than_or_equal_to.format_statement(x=1, y=1)
    ) == less_than_or_equal_to(1, 1)
    assert eval(
        less_than_or_equal_to.format_statement(x=2, y=1)
    ) == less_than_or_equal_to(2, 1)


def test_not_in():
    assert not_in("a", "hello") is True
    assert not_in("e", "hello") is False
    assert not_in("e", ["e", "a"]) is False
    assert not_in("bye", ["hello"]) is True

    assert not_in.statement == "x not in y"

    assert eval(not_in.format_statement(x="a", y="hello")) == not_in("a", "hello")
    assert eval(not_in.format_statement(x="e", y="hello")) == not_in("e", "hello")
    assert eval(not_in.format_statement(x="e", y=["e", "a"])) == not_in("e", ["e", "a"])
    assert eval(not_in.format_statement(x="bye", y=["hello"])) == not_in(
        "bye", ["hello"]
    )
