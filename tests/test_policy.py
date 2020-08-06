import pytest

from password_validation.character_pool import CharacterPool
from password_validation.funcs import greater_than_or_equal_to
from password_validation.funcs import less_than_or_equal_to
from password_validation.funcs import not_in
from password_validation.policy import MakePasswordRequirement
from password_validation.policy import PasswordPolicy
from password_validation.policy import PasswordRequirement


def test_make_password_requirement():
    requirement = MakePasswordRequirement("name", 5)
    assert requirement
    assert isinstance(requirement, MakePasswordRequirement)
    assert requirement.name == "name"
    assert requirement.requirement == 5
    assert requirement.func == greater_than_or_equal_to


def test_password_requirement():
    password_requirement = PasswordRequirement("hello", 0, 1, greater_than_or_equal_to)

    # check object
    assert isinstance(password_requirement, PasswordRequirement)

    # check attrs
    assert password_requirement.name == "hello"
    assert password_requirement.requirement == 1
    assert password_requirement.actual == 0
    assert password_requirement.func == greater_than_or_equal_to

    # should be false because requirement isn't satisfied
    assert not password_requirement
    assert not bool(password_requirement)

    password_requirement = PasswordRequirement("hello", 10, 1, greater_than_or_equal_to)
    assert password_requirement


def test_password_requirement_ge():
    password_requirement = PasswordRequirement("hello", 1, 10, greater_than_or_equal_to)
    assert not password_requirement

    password_requirement = PasswordRequirement("hello", 10, 1, greater_than_or_equal_to)
    assert password_requirement


def test_password_requirement_le():
    password_requirement = PasswordRequirement("hello", 10, 1, less_than_or_equal_to)
    assert not password_requirement

    password_requirement = PasswordRequirement("hello", 1, 10, less_than_or_equal_to)
    assert password_requirement


def test_password_requirement_not_in():
    password_requirement = PasswordRequirement("hello", "hello", [], not_in)
    assert password_requirement

    password_requirement = PasswordRequirement("hello", "hello", ["what"], not_in)
    assert password_requirement

    password_requirement = PasswordRequirement("hello", "hello", ["hello"], not_in)
    assert not password_requirement

    password_requirement = PasswordRequirement("hello", "h", "ello", not_in)
    assert password_requirement

    password_requirement = PasswordRequirement("hello", "h", "hello", not_in)
    assert not password_requirement


def test_make_password_requirement_le():
    max_len_requirement = MakePasswordRequirement(
        "max_len", 10, func=less_than_or_equal_to
    )
    assert max_len_requirement

    req = max_len_requirement(15)
    assert not req


def test_make_password_requirement_contains():
    forbidden_words = ["hello", "world"]
    forbidden_requirements = MakePasswordRequirement(
        "forbidden words", forbidden_words, func=not_in
    )
    assert forbidden_requirements

    req = forbidden_requirements("wtf")
    assert req

    req = forbidden_requirements("hello")
    assert not req

    req = forbidden_requirements("world")
    assert not req

    req = forbidden_requirements("bye")
    assert req


def test_make_password_requirement_contains_empty_list():
    forbidden_words = []
    forbidden_requirements = MakePasswordRequirement(
        "forbidden words", forbidden_words, func=not_in
    )
    assert forbidden_requirements

    req = forbidden_requirements("wtf")
    assert req
    req = forbidden_requirements("hello")
    assert req
    req = forbidden_requirements("world")
    assert req
    req = forbidden_requirements("bye")
    assert req


def test_make_password_requirement_different_domain():
    func = lambda x, y: True if x == "hello" else False
    password_requirement = MakePasswordRequirement("hello", "world", func)

    assert password_requirement

    req = password_requirement("hello")
    assert req

    req = password_requirement("bye")
    assert not req


def test_password_policy():
    # check object
    policy = PasswordPolicy()
    assert policy
    assert isinstance(policy, PasswordPolicy)

    # check attrs
    assert policy.lowercase == 0
    assert policy.uppercase == 0
    assert policy.symbols == 0
    assert policy.numbers == 0
    assert policy.whitespace == 0
    assert policy.other == 0
    assert policy.min_length == 12
    assert policy.max_length == 128
    assert policy.min_entropy == 32
    assert policy.classification == "Weak"
    assert policy.forbidden_words == []
    assert policy.pool

    assert policy.to_dict()
    assert isinstance(policy.to_dict(), dict)
    assert policy.to_dict() == dict(
        lowercase=0,
        uppercase=0,
        symbols=0,
        numbers=0,
        whitespace=0,
        other=0,
        min_length=12,
        max_length=128,
        entropy=32,
        classification="Weak",
        forbidden_words=[],
        character_pool=CharacterPool().to_dict(),
    )


def test_policy_with_entropy():
    policy = PasswordPolicy(min_length=0)

    failures = policy.test_password("hel")
    assert len(failures) == 1


def test_password_policy_other_kwargs():
    # check object
    policy = PasswordPolicy(
        lowercase=1,
        uppercase=2,
        symbols=3,
        numbers=4,
        whitespace=1,
        min_length=24,
        max_length=64,
    )
    assert policy
    assert isinstance(policy, PasswordPolicy)

    # check attrs
    assert policy.lowercase == 1
    assert policy.uppercase == 2
    assert policy.symbols == 3
    assert policy.numbers == 4
    assert policy.whitespace == 1
    assert policy.min_length == 24
    assert policy.max_length == 64
    assert policy.pool


def test_password_policy_breaks_lowercase():
    # 0 to 26 are all acceptable values
    for i in range(0, 27):
        assert PasswordPolicy(lowercase=i)

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=27)

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase="1")

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=2.5)


def test_password_policy_breaks_uppercase():
    # 0 to 26 are all acceptable values
    for i in range(0, 27):
        assert PasswordPolicy(uppercase=i)

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase=27)

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase="1")

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase=2.5)


def test_password_policy_breaks_numbers():
    # 0 to 9 are all acceptable values
    for i in range(0, 10):
        assert PasswordPolicy(numbers=i)

    with pytest.raises(AssertionError):
        PasswordPolicy(numbers=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(numbers=11)

    with pytest.raises(AssertionError):
        PasswordPolicy(numbers="3")

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=[1, 2, 3])


def test_password_policy_breaks_symbols():
    # 0 to 32 acceptable symbols
    for i in range(0, 33):
        assert PasswordPolicy(symbols=i)

    with pytest.raises(AssertionError):
        PasswordPolicy(symbols=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(symbols=33)

    with pytest.raises(AssertionError):
        PasswordPolicy(symbols="33")

    with pytest.raises(AssertionError):
        PasswordPolicy(symbols=b"d")


def test_password_policy_breaks_whitespace():
    # 0 to 6 acceptable whitespace
    for i in range(0, 7):
        assert PasswordPolicy(symbols=i)

    with pytest.raises(AssertionError):
        PasswordPolicy(whitespace=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(whitespace=7)

    with pytest.raises(AssertionError):
        PasswordPolicy(whitespace=" ")

    with pytest.raises(AssertionError):
        PasswordPolicy(whitespace={})


def test_password_policy_breaks_other():
    assert PasswordPolicy(other=0)

    with pytest.raises(AssertionError):
        PasswordPolicy(other=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(other=1)

    with pytest.raises(AssertionError):
        PasswordPolicy(other="33")

    with pytest.raises(AssertionError):
        PasswordPolicy(other=b"d")


def test_password_policy_breaks_min_and_max_length():
    with pytest.raises(AssertionError):
        PasswordPolicy(min_length="1")

    with pytest.raises(AssertionError):
        PasswordPolicy(max_length=1.2)

    with pytest.raises(AssertionError):
        PasswordPolicy(min_length=-1)

    with pytest.raises(AssertionError):
        PasswordPolicy(min_length=10, max_length=5)


def test_password_policy_with_hex_character_pool(hex_pool):
    policy = PasswordPolicy(character_pool=hex_pool)
    assert policy
    assert isinstance(policy, PasswordPolicy)

    # check attrs
    assert policy.lowercase == 0
    assert policy.uppercase == 0
    assert policy.symbols == 0
    assert policy.numbers == 0
    assert policy.whitespace == 0
    assert policy.other == 0
    assert policy.min_length == 12
    assert policy.max_length == 128
    assert policy.pool


def test_password_policy_breaks_lowercase_with_hex_pool(hex_pool):
    # 0 to 7 are all acceptable values
    for i in range(0, 7):
        assert PasswordPolicy(lowercase=i, character_pool=hex_pool)

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=-1, character_pool=hex_pool)

    with pytest.raises(AssertionError):
        PasswordPolicy(lowercase=7, character_pool=hex_pool)


def test_password_policy_breaks_uppercase_with_hex_pool(hex_pool):
    # 0 to 7 are all acceptable values
    for i in range(0, 7):
        assert PasswordPolicy(uppercase=i, character_pool=hex_pool)

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase=-1, character_pool=hex_pool)

    with pytest.raises(AssertionError):
        PasswordPolicy(uppercase=7, character_pool=hex_pool)


def test_password_policy_with_random_pool(random_pool):
    # check object
    policy = PasswordPolicy(character_pool=random_pool)
    assert policy
    assert isinstance(policy, PasswordPolicy)

    # check attrs
    assert policy.lowercase == 0
    assert policy.uppercase == 0
    assert policy.symbols == 0
    assert policy.numbers == 0
    assert policy.whitespace == 0
    assert policy.other == 0
    assert policy.min_length == 12
    assert policy.max_length == 128
    assert policy.pool


def test_password_policy_breaks_lowercase_with_random_pool(random_pool):
    for i in range(0, len(random_pool.lowercase) + 1):
        assert PasswordPolicy(lowercase=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(
            lowercase=len(random_pool.lowercase) + 1, character_pool=random_pool
        )


def test_password_policy_breaks_uppercase_with_random_pool(random_pool):
    for i in range(0, len(random_pool.uppercase) + 1):
        assert PasswordPolicy(uppercase=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(
            uppercase=len(random_pool.uppercase) + 1, character_pool=random_pool
        )


def test_password_policy_breaks_numbers_with_random_pool(random_pool):
    for i in range(0, len(random_pool.numbers) + 1):
        assert PasswordPolicy(numbers=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(numbers=len(random_pool.numbers) + 1, character_pool=random_pool)


def test_password_policy_breaks_symbols_with_random_pool(random_pool):
    for i in range(0, len(random_pool.symbols) + 1):
        assert PasswordPolicy(symbols=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(symbols=len(random_pool.symbols) + 1, character_pool=random_pool)


def test_password_policy_breaks_whitespace_with_random_pool(random_pool):
    for i in range(0, len(random_pool.whitespace) + 1):
        assert PasswordPolicy(symbols=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(
            whitespace=len(random_pool.whitespace) + 1, character_pool=random_pool
        )


def test_password_policy_breaks_other_with_random_pool(random_pool):
    for i in range(0, len(random_pool.other) + 1):
        assert PasswordPolicy(other=i, character_pool=random_pool)
    with pytest.raises(AssertionError):
        PasswordPolicy(other=len(random_pool.other) + 1, character_pool=random_pool)
