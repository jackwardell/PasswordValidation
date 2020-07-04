import math

from password_entropy.character_pool import CharacterPool
from password_entropy.character_pool import lenient_pool_of_unique_characters
from password_entropy.character_pool import normal_pool_of_unique_characters
from password_entropy.character_pool import strict_pool_of_unique_characters
from password_entropy.exceptions import UnacceptableCharacters, ClassificationError


def calculate_number_of_possible_passwords(
        password: str, method: str = "normal", character_pool: CharacterPool = None
):
    """

    :param password:
    :param method:
    :param character_pool:
    :return:
    """
    if character_pool is None:
        pool = CharacterPool()
    else:
        pool = character_pool

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

    return pool_of_characters ** len(password)


def calculate_entropy(
        password: str, method: str = "normal", character_pool: CharacterPool = None
):
    """

    :param password:
    :param method:
    :param character_pool:
    :return:
    """
    if character_pool is None:
        pool = CharacterPool()
    else:
        pool = character_pool

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
            end = float('inf')
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


class Classifier:
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

    def validate_ranges(self):
        ranges = sorted([i for j in self.ranges for i in j])
        start, end = ranges.pop(0), ranges.pop(-1)
        assert start == 0, "start must be 0"
        assert end > start, "end must be greater than start"

        for c, (i, j) in enumerate([r.to_tuple() for r in self.ranges]):
            if c == 0:
                assert i == 0, "start must be 0"
            else:
                pass

    def classify(self, value):
        results = [k for k, v in self.ranges.items() if value in v]
        if len(results) >= 0:
            raise ClassificationError(f"value fits into {len(results)} provided entropy ranges. It should be 1.")
        else:
            return results.pop()
