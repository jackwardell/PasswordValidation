import pytest

from password_entropy.password import Password


def test_password():
    password = Password("hello world")

    # quick check on object
    assert password
    assert isinstance(password, Password)

    # check attrs
    assert password.lowercase == 10
    assert password.whitespace == 1
    assert password.length == 11

    assert password.uppercase == 0
    assert password.other == 0
    assert password.symbols == 0

    assert isinstance(password.entropy, (int, float))


def test_password_breaks(hex_pool):
    with pytest.raises(AssertionError):
        Password("hello world", character_pool=hex_pool)


def test_another_password():
    password = Password("Hello World 12345 !")

    # quick check on object
    assert password
    assert isinstance(password, Password)

    # check attrs
    assert password.lowercase == 8
    assert password.whitespace == 3
    assert password.length == 19

    assert password.uppercase == 2
    assert password.other == 0
    assert password.symbols == 1

    assert isinstance(password.entropy, (int, float))
