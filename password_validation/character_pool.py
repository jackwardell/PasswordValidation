class CharacterPool:
    """
    The pool of characters to make a password from.

    The default pool is ascii characters, it was taken from the string built-in
    library.

    defaults:
    lowercase = abcdefghijklmnopqrstuvwxyz
    uppercase = ABCDEFGHIJKLMNOPQRSTUVWXYZ
    numbers = 0123456789
    symbols = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    whitespace =

    other is a space where you can put other values if you wanted extra chars

    This class can be passed different values if you wanted to use for, say,
    another non-english alphabet.

    :param lowercase: the lowercase characters
    :type: str
    :default: abcdefghijklmnopqrstuvwxyz


    """
    def __init__(
        self,
        lowercase: str = "abcdefghijklmnopqrstuvwxyz",
        uppercase: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        numbers: str = "0123456789",
        symbols: str = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""",
        whitespace: str = " ",
        other: str = "",
    ):
        self.lowercase = set(lowercase)
        self.uppercase = set(uppercase)
        self.numbers = set(numbers)
        self.symbols = set(symbols)
        self.whitespace = set(whitespace)
        self.other = set(other)
        self.letters = self.lowercase | self.uppercase
        self.alphanumeric = self.letters | self.numbers
        self.all = self.alphanumeric | self.symbols | self.whitespace | self.other

    def to_dict(self) -> dict:
        rv = {
            "lowercase": self.lowercase,
            "uppercase": self.uppercase,
            "numbers": self.numbers,
            "symbols": self.symbols,
            "whitespace": self.whitespace,
            "other": self.other,
        }
        return rv


def strict_pool_of_unique_characters(word):
    return len(set(word))


def normal_pool_of_unique_characters(word, character_pool=None):
    # set pool if not passed
    if character_pool is None:
        pool = CharacterPool()
    else:
        pool = character_pool

    # set unique characters to 01
    unique_characters = 0
    # turn word into set of characters
    characters = set(word)

    # get intersections for lowercase
    if characters & pool.lowercase:
        unique_characters += len(pool.lowercase)
    # get intersections for uppercase
    if characters & pool.uppercase:
        unique_characters += len(pool.uppercase)
    # get intersections for numbers
    if characters & pool.numbers:
        unique_characters += len(pool.numbers)
    # get intersections for symbols
    if characters & pool.symbols:
        unique_characters += len(pool.symbols)
    # get intersections for whitespace
    if characters & pool.whitespace:
        unique_characters += len(pool.whitespace)
    # get intersections for other
    if characters & pool.other:
        unique_characters += len(pool.other)

    return unique_characters


def lenient_pool_of_unique_characters(character_pool=None):
    # set pool if not passed
    if character_pool is None:
        pool = CharacterPool()
    else:
        pool = character_pool

    return len(pool.all)
