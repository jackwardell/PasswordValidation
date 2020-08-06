import operator
import typing
from typing import Any

from password_validation.character_pool import CharacterPool
from password_validation.funcs import greater_than_or_equal_to
from password_validation.funcs import less_than_or_equal_to
from password_validation.calculate import Classifier
from password_validation.funcs import not_in
from password_validation.password import Password


def _make_password(password):
    if isinstance(password, str):
        return Password(password)
    elif isinstance(password, Password):
        return password
    else:
        raise ValueError("password must be str or Password")


class PasswordRequirement:
    def __init__(
        self, name: str, actual: Any, requirement: Any, func: operator,
    ):
        self.name = name
        self.requirement = requirement
        self.actual = actual
        self.func = func

    def __bool__(self):
        return self.func(self.actual, self.requirement)

    def __repr__(self):
        message = (
            f"<Requirement{'F' if self else 'Unf'}ulfilled('{self.name}', "
            f"statement=({self.func.format_statement(x=self.actual, y=self.requirement)}))>"
            # f"expected={self.requirement}, got={self.actual}, "
            # f"operation={self.func.__qualname__}({self.actual}, {self.requirement}))>"
        )
        return message


class MakePasswordRequirement:
    def __init__(
        self,
        name: str,
        requirement: typing.Any,
        func: operator = greater_than_or_equal_to,
        cls: PasswordRequirement = None,
    ):
        self.name = name
        self.requirement = requirement
        self.func = func
        if cls is None:
            self.cls = PasswordRequirement
        else:
            self.cls = cls

    def __call__(self, actual):
        cls = self.cls(self.name, actual, self.requirement, self.func)
        return cls


class PasswordPolicy:
    """
    The password policy is where one can define what they expect of a password
    when submitted by a user.

    The default policy, is that a user chooses a password of at least 12
    characters, but there is no requirement to use an amount of particular
    character types, e.g. symbols

    :param lowercase (int): the minimum number of lowercase characters in a
                            password
    :param uppercase (int): the minimum number of uppercase characters in a
                            password
    :param symbols (int): the minimum number of symbol characters in a password
    :param numbers (int): the minimum number of number characters in a password
    :param other (int): the minimum number of other characters in a password
    :param whitespace (int): the minimum number of whitespace characters in a
                             password
    :param min_length (int): the minimum length for a password
    :param max_length (int): the maximum length for a password
    :param forbidden_words (list(str)): a list of forbidden words as strings
    :param character_pool (CharacterPool): the pool or characters to pick from
    """

    def __init__(
        self,
        lowercase: int = 0,
        uppercase: int = 0,
        symbols: int = 0,
        numbers: int = 0,
        whitespace: int = 0,
        other: int = 0,
        min_length: int = 12,
        max_length: int = 128,
        min_entropy: typing.Union[int, float] = 32,
        forbidden_words: list = None,
        character_pool: CharacterPool = None,
        requirement_cls: PasswordRequirement = None,
        classifier: Classifier = None,
    ):
        # set character pool if not passed
        if character_pool is None:
            self.pool = CharacterPool()
        else:
            self.pool = character_pool

        # set requirement class if not passed
        if requirement_cls is None:
            self.requirement_cls = PasswordRequirement
        else:
            self.requirement_cls = requirement_cls

        # check lowercase value acceptable
        # first check is int
        assert isinstance(
            lowercase, int
        ), "lowercase (the minimum number of lowercase characters) must be int"
        # then check it is a value between 0 and the number of
        # lowercase characters in the character pool (ascii is 0-26)
        assert 0 <= lowercase <= len(self.pool.lowercase), (
            f"lowercase (the minimum number of lowercase characters) must be "
            f"between 0 and {len(self.pool.lowercase)} inclusive"
        )
        self.lowercase = lowercase
        self.lowercase_requirement = MakePasswordRequirement(
            "the minimum number of lowercase characters",
            self.lowercase,
            cls=requirement_cls,
        )

        # check uppercase value acceptable
        # first check is int
        assert isinstance(
            uppercase, int
        ), "uppercase (the minimum number of uppercase characters) must be int"
        # then check it is a value between 0 and the number of
        # lowercase characters in the character pool (ascii is 0-26)
        assert 0 <= uppercase <= len(self.pool.uppercase), (
            f"uppercase (the minimum number of uppercase characters) must be "
            f"between 0 and {len(self.pool.uppercase)} inclusive"
        )
        self.uppercase = uppercase
        self.uppercase_requirement = MakePasswordRequirement(
            "the minimum number of uppercase characters",
            self.uppercase,
            cls=requirement_cls,
        )

        # check numbers value acceptable
        # first check is int
        assert isinstance(
            numbers, int
        ), "numbers (the minimum number of number characters) must be int"
        # then check it is a value between 0 and the number of
        # number characters in the character pool (ascii is 0-9)
        assert 0 <= numbers <= len(self.pool.numbers), (
            f"numbers (the minimum number of number characters) must be "
            f"between 0 and {len(self.pool.numbers)} inclusive"
        )
        self.numbers = numbers
        self.numbers_requirement = MakePasswordRequirement(
            "the minimum number of number characters", self.numbers, cls=requirement_cls
        )

        # check symbols value acceptable
        # first check is int
        assert isinstance(
            symbols, int
        ), "symbols (the minimum number of symbol characters) must be int"
        # then check it is a value between 0 and the number of
        # number characters in the character pool (ascii is 0-32)
        # although for symbols this is debatable, some might not include
        # particular symbol characters like '\' or ';', etc
        # this is overridable, like all pool features depending on use case
        assert 0 <= symbols <= len(self.pool.symbols), (
            f"symbols (the minimum number of symbol characters) must be "
            f"between 0 and {len(self.pool.symbols)} inclusive"
        )
        self.symbols = symbols
        self.symbols_requirement = MakePasswordRequirement(
            "the minimum number of symbol characters", self.symbols, cls=requirement_cls
        )

        # check whitespace value acceptable
        # first check is int
        assert isinstance(whitespace, int), (
            "whitespace (the minimum number of whitespace characters) must be " "int"
        )
        # then check it is a value between 0 and the number of
        # number characters in the character pool (ascii is 0-5)
        assert 0 <= whitespace <= len(self.pool.whitespace), (
            f"whitespace (the minimum number of whitespace characters) must be "
            f"between 0 and {len(self.pool.whitespace)} inclusive"
        )
        self.whitespace = whitespace
        self.whitespace_requirement = MakePasswordRequirement(
            "the minimum number of whitespace characters",
            self.whitespace,
            cls=requirement_cls,
        )

        # check other value acceptable
        # first check is int
        assert isinstance(
            other, int
        ), "other (the minimum number of other characters) must be int"
        # then check it is a value between 0 and the number of
        # other characters in the character pool (ascii is 0)
        # this can be used as a bucket by developers that want to allow
        # other characters
        assert 0 <= other <= len(self.pool.other), (
            f"other (the minimum number of other characters) must be "
            f"between 0 and {len(self.pool.other)} inclusive"
        )
        self.other = other
        self.other_requirement = MakePasswordRequirement(
            "the minimum number of other characters", self.other, cls=requirement_cls
        )

        # check min_length value acceptable
        # check is int
        assert isinstance(
            min_length, int
        ), "min_length (the minimum password length) must be int"
        # check max_length value acceptable
        # check is int
        assert isinstance(
            max_length, int
        ), "max_length (the maximum password length) must be int"
        # then check one is
        assert 0 <= min_length <= max_length, (
            "the min_length (minimum password length) cannot be smaller than "
            "the max_length (maximum password length) and must be larger than "
            "0. However the min_length and max_length can be equal if the user "
            "desires a single length for all passwords"
        )
        self.min_length = min_length
        self.min_length_requirement = MakePasswordRequirement(
            "the minimum password length", self.min_length, cls=requirement_cls,
        )

        self.max_length = max_length
        self.max_length_requirement = MakePasswordRequirement(
            "the maximum password length",
            self.max_length,
            func=less_than_or_equal_to,
            cls=requirement_cls,
        )

        assert isinstance(min_entropy, (int, float)), "entropy must be an int or float"
        assert 0 < min_entropy, "entropy must be greater than 0"
        self.min_entropy = min_entropy
        self.entropy_requirement = MakePasswordRequirement(
            "entropy", self.min_entropy, cls=requirement_cls
        )

        self.forbidden_words = forbidden_words if forbidden_words else []
        assert isinstance(self.forbidden_words, list), "forbidden words must be a list"
        for word in self.forbidden_words:
            assert isinstance(word, str), "all forbidden words must be strings"
        self.forbidden_words_requirements = MakePasswordRequirement(
            "forbidden words", self.forbidden_words, cls=requirement_cls, func=not_in,
        )

        # set a classifier if not passed
        # with default values of:
        # "Very Weak" is entropy between 0 to 28
        # "Weak" is entropy between 28 to 35
        # "Ok" is entropy between 35 to 59
        # "Good" is entropy between 59 to 127
        # "Very Good" is entropy above 127
        if classifier is None:
            self.classifier = Classifier()
        else:
            self.classifier = classifier

        # set a classification level from the entropy value
        self.classification = self.classifier.classify(self.min_entropy)

    def to_dict(self) -> dict:
        rv = {
            "lowercase": self.lowercase,
            "uppercase": self.uppercase,
            "symbols": self.symbols,
            "numbers": self.numbers,
            "whitespace": self.whitespace,
            "other": self.other,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "entropy": self.min_entropy,
            "forbidden_words": self.forbidden_words,
            "classification": self.classification,
            "character_pool": self.pool.to_dict(),
        }
        return rv

    def test_password(self, password: str, failures_only: bool = True):
        password = _make_password(password)
        validity = [
            self.lowercase_requirement(password.lowercase),
            self.uppercase_requirement(password.uppercase),
            self.numbers_requirement(password.numbers),
            self.symbols_requirement(password.symbols),
            self.whitespace_requirement(password.whitespace),
            self.other_requirement(password.other),
            self.min_length_requirement(password.length),
            self.max_length_requirement(password.length),
            self.entropy_requirement(password.entropy),
            self.forbidden_words_requirements(password.password),
        ]
        return [i for i in validity if not i] if failures_only else validity

    def validate(self, password):
        return not bool(self.test_password(password))
