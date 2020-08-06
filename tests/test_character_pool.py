from password_validation.character_pool import CharacterPool

from password_validation.character_pool import lenient_pool_of_unique_characters
from password_validation.character_pool import normal_pool_of_unique_characters
from password_validation.character_pool import strict_pool_of_unique_characters


def test_character_pool():
    pool = CharacterPool()

    assert pool.lowercase == set("abcdefghijklmnopqrstuvwxyz")
    assert pool.uppercase == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert pool.numbers == set("0123456789")
    assert pool.symbols == set(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
    assert pool.whitespace == set(" ")
    assert pool.other == set()
    assert pool.letters == pool.lowercase | pool.uppercase
    assert pool.alphanumeric == pool.letters | pool.numbers
    assert pool.all == pool.alphanumeric | pool.symbols | pool.whitespace | pool.other


# def test_character_pool_init_default():
#     pool = CharacterPool()
#
#     assert pool.lowercase == set("abcdefghijklmnopqrstuvwxyz")
#     assert pool.uppercase == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
#     assert pool.numbers == set("0123456789")
#     assert pool.symbols == set(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
#     assert pool.whitespace == set(" \t\n\r\v\f")
#     assert pool.other == set()
#     assert pool.letters == pool.lowercase | pool.uppercase
#     assert pool.alphanumeric == pool.letters | pool.numbers
#     assert pool.all == pool.alphanumeric | pool.symbols | pool.whitespace | pool.other


def test_character_pool_init_with_kwargs():
    pool = CharacterPool(
        lowercase="abc",
        uppercase="XYZ",
        numbers="123",
        symbols="()",
        whitespace=" ",
        other="é",
    )

    assert pool.lowercase == set("abc")
    assert pool.uppercase == set("XYZ")
    assert pool.numbers == set("123")
    assert pool.symbols == set("()")
    assert pool.whitespace == set(" ")
    assert pool.other == set("é")
    assert pool.letters == pool.lowercase | pool.uppercase
    assert pool.alphanumeric == pool.letters | pool.numbers
    assert pool.all == pool.alphanumeric | pool.symbols | pool.whitespace | pool.other


def test_strict_evaluation():
    pool = CharacterPool()

    password = "abcdefghij"
    assert strict_pool_of_unique_characters(password) == len(password)
    assert strict_pool_of_unique_characters(password) == 10

    password = "aaa bbb ccc"
    assert strict_pool_of_unique_characters(password) == len(set(password))
    assert strict_pool_of_unique_characters(password) == 4

    password = "AaBbCc"
    assert strict_pool_of_unique_characters(password) == 6

    password = "0123456789"
    assert strict_pool_of_unique_characters(password) == 10

    password = "Hello World 1234"
    assert strict_pool_of_unique_characters(password) == 12

    password = "0123456789!!!!!!!!"
    assert strict_pool_of_unique_characters(password) == 11

    password = pool.lowercase
    assert strict_pool_of_unique_characters(password) == len(pool.lowercase)
    assert strict_pool_of_unique_characters(password) == 26

    password = pool.uppercase
    assert strict_pool_of_unique_characters(password) == len(pool.uppercase)
    assert strict_pool_of_unique_characters(password) == 26

    password = pool.numbers
    assert strict_pool_of_unique_characters(password) == len(pool.numbers)
    assert strict_pool_of_unique_characters(password) == 10

    password = pool.whitespace
    assert strict_pool_of_unique_characters(password) == len(pool.whitespace)
    assert strict_pool_of_unique_characters(password) == 1

    password = pool.symbols
    assert strict_pool_of_unique_characters(password) == len(pool.symbols)
    assert strict_pool_of_unique_characters(password) == 32


def test_normal_evaluation_singles():
    pool = CharacterPool()
    # singles
    password = "a"
    assert normal_pool_of_unique_characters(password) == len(pool.lowercase)
    assert normal_pool_of_unique_characters(password) == 26

    password = "A"
    assert normal_pool_of_unique_characters(password) == len(pool.uppercase)
    assert normal_pool_of_unique_characters(password) == 26

    password = "."
    assert normal_pool_of_unique_characters(password) == len(pool.symbols)
    assert normal_pool_of_unique_characters(password) == 32

    password = "1"
    assert normal_pool_of_unique_characters(password) == len(pool.numbers)
    assert normal_pool_of_unique_characters(password) == 10

    password = " "
    assert normal_pool_of_unique_characters(password) == len(pool.whitespace)
    assert normal_pool_of_unique_characters(password) == 1


def test_normal_evaluation_doubles():
    pool = CharacterPool()
    # doubles
    password = "a."
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.symbols
    )
    assert normal_pool_of_unique_characters(password) == 26 + 32

    password = "Hello"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.uppercase
    )
    assert normal_pool_of_unique_characters(password) == len(pool.letters)
    assert normal_pool_of_unique_characters(password) == 26 + 26

    password = "hello123"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 26 + 10

    password = "hello!"
    assert normal_pool_of_unique_characters(password) == len(
        pool.uppercase | pool.symbols
    )
    assert normal_pool_of_unique_characters(password) == 26 + 32

    password = "HELLO123"
    assert normal_pool_of_unique_characters(password) == len(
        pool.uppercase | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 26 + 10

    password = "HELLO123"
    assert normal_pool_of_unique_characters(password) == len(
        pool.uppercase | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 26 + 10


def test_normal_evaluation_triples():
    pool = CharacterPool()
    # triples
    password = "Hello@world"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.uppercase | pool.symbols
    )
    assert normal_pool_of_unique_characters(password) == 26 + 26 + 32

    password = "Hello1234"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.uppercase | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == len(pool.alphanumeric)
    assert normal_pool_of_unique_characters(password) == 26 + 26 + 10

    password = "hello!world1234"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase | pool.symbols | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 26 + 32 + 10
    #
    password = "h!ello1234"
    assert normal_pool_of_unique_characters(password) == len(
        pool.uppercase | pool.symbols | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 26 + 32 + 10


def test_normal_evaluation_quadruples():
    pool = CharacterPool()
    # quadruple
    password = "HelloWorld234$"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase
        | pool.uppercase
        | pool.symbols
        | pool.numbers
    )
    assert normal_pool_of_unique_characters(password) == 94


def test_normal_evaluation_quintuple():
    pool = CharacterPool()
    # quadruple
    password = "Hello World 1234$"
    assert normal_pool_of_unique_characters(password) == len(
        pool.lowercase
        | pool.uppercase
        | pool.symbols
        | pool.numbers
        | pool.whitespace
    )
    assert normal_pool_of_unique_characters(password) == len(pool.all)
    assert normal_pool_of_unique_characters(password) == 95


def test_lenient_evaluation():
    pool = CharacterPool()
    assert lenient_pool_of_unique_characters() == len(pool.all)
    assert lenient_pool_of_unique_characters() == 95
