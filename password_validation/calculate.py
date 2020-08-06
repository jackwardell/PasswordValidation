import math

from password_validation.character_pool import CharacterPool
from password_validation.character_pool import lenient_pool_of_unique_characters
from password_validation.character_pool import normal_pool_of_unique_characters
from password_validation.character_pool import strict_pool_of_unique_characters
from password_validation.exceptions import UnacceptableCharacters, ClassificationError
from typing import Union


def calculate_number_of_possible_passwords(
        password: str, method: str = "normal", character_pool: CharacterPool = None
):
    """
    Calculate the number of possible passwords according to the formula:
    size of pool of characters (int) ^ number of characters in password (int)

    :param password: the password
    :type: str

    :param method: method to calculate the pool of characters
    :type: str ("strict", "normal" or "lenient")

    :param character_pool: pool of characters to use
    :type: CharacterPool

    :return: Number Of Possible Passwords
    :type: int
    """
    # set default char pool if user doesn't pass one
    if character_pool is None:
        pool = CharacterPool()
    # else set user char pool, should be init'd or have viable class methods
    else:
        pool = character_pool

    # user can pick between strict, normal and lenient
    if method == "strict":
        pool_of_characters = strict_pool_of_unique_characters(password)
    elif method == "normal":
        pool_of_characters = normal_pool_of_unique_characters(
            password, character_pool=pool
        )
    elif method == "lenient":
        pool_of_characters = lenient_pool_of_unique_characters(character_pool=pool)
    else:
        raise ValueError('method must be either "strict", "normal" or "lenient"')

    # return pool of chars ^ len password
    return pool_of_characters ** len(password)


def calculate_entropy(
        password: str, method: str = "normal", character_pool: CharacterPool = None
):
    """
    Calculate the entropy of a password according to the formula:
    log base 2 (number of possible passwords)

    :param password: the password
    :type: str

    :param method: method to calculate the pool of characters
    :type: str ("strict", "normal" or "lenient")

    :param character_pool: pool of characters to use
    :type: CharacterPool

    :return: Entropy of password
    :type: float
    """
    # set default char pool if user doesn't pass one
    if character_pool is None:
        pool = CharacterPool()
    # else set user char pool, should be init'd or have viable class methods
    else:
        pool = character_pool

    # all chars must be in password char pool
    if not all(i in pool.all for i in password):
        raise UnacceptableCharacters(
            f"You can only use characters from the character pool, "
            f"which are: {pool.all}"
        )
    else:
        number_of_possible_passwords = calculate_number_of_possible_passwords(
            password, method, pool
        )
        return math.log(number_of_possible_passwords, 2)


class EntropyRange:
    """
    Essentially a range object, with fewer features.

    Built-in range objects can't handle floats.

    Aim of this class is to represent a range of values.
        e.g. EntropyRange(0, 35) would be a range between 0 and 35.
             inclusive of 35 but not of 0. This is slightly different behaviour
             to built-in ranges.

        therefore:
            > 0 in EntropyRange(0, 35)
            False
            > 1 in EntropyRange(0, 35)
            True
            > 35 in EntropyRange(0, 35)
            True

        but also:
            > 34.35 in EntropyRange(0, 35)
            True

        where as:
            > 34.35 in range(0, 35)
            False

    :param beginning: beginning value of the range
    :type: int

    :param end: end value of the range
    :type: int
    """

    def __init__(self, beginning, end):
        assert isinstance(
            beginning, (int, float)
        ), "beginning range value must be a number (int or float)"
        if end is not None:
            assert isinstance(
                end, (int, float)
            ), "end range value must be a number (int or float)"
            assert (
                    beginning <= end
            ), "end value must be greater than or equal to the beginning value"
        else:
            end = float("inf")
        self.beginning = beginning
        self.end = end
        self.beginning_end = self.beginning, self.end

    def __contains__(self, value):
        rv = self.beginning < value <= self.end if self.end else self.beginning < value
        return rv

    def __iter__(self):
        return iter(self.beginning_end)

    def to_tuple(self):
        return self.beginning_end

    def __repr__(self):
        return f"EntropyRange({self.beginning}, {self.end})"

    def __eq__(self, other):
        return type(self) == type(other) and self.beginning_end == other.beginning_end


class Classifier:
    """
    A classifier for entropy.

    Aim of this class is to classify a value (which in this instance is the
    entropy).
        e.g.
        > classifier = Classifier()
        > classifier.classify(56.554)
        'Ok'

    The class comes with default values for password classification (see below).
    But they can be overridden by passing a dict of EntropyRanges in.

    :param ranges: dict of range values
                   e.g. {"Bad": EntropyRange(0,100),
                         "Good": EntropyRange(100, 1000)}
    :type: dict

    """
    default_ranges = {
        "Very Weak": EntropyRange(0, 28),
        "Weak": EntropyRange(28, 35),
        "Ok": EntropyRange(35, 59),
        "Good": EntropyRange(59, 127),
        "Very Good": EntropyRange(127, None),
    }

    def __init__(self, ranges: dict = None):
        if not ranges:
            self.ranges = self.default_ranges
        else:
            self.ranges = ranges

    # todo: validate the ranges
    # def validate_ranges(self):
    #     ranges = sorted([i for j in self.ranges for i in j])
    #     start, end = ranges.pop(0), ranges.pop(-1)
    #     assert start == 0, "start must be 0"
    #     assert end > start, "end must be greater than start"
    #
    #     for c, (i, j) in enumerate([r.to_tuple() for r in self.ranges]):
    #         if c == 0:
    #             assert i == 0, "start must be 0"
    #         else:
    #             pass

    def classify(self, value: Union[int, float]) -> str:
        """
        classify a value

        :param value: a number
        :type: int or float

        :return: the classification
        :type: str
        """
        results = [k for k, v in self.ranges.items() if value in v]
        if len(results) != 1:
            raise ClassificationError(
                f"value fits into {len(results)} provided entropy ranges. "
                f"It should be 1."
            )
        else:
            return results.pop()
