import pytest

from password_validation.character_pool import CharacterPool


@pytest.fixture
def hex_pool():
    pool = CharacterPool(
        lowercase="abcdef", uppercase="ABCDEF", symbols="", whitespace=""
    )
    yield pool


@pytest.fixture
def random_pool():
    pool = CharacterPool(
        lowercase="123xyz",
        uppercase="ABC!",
        symbols="<@>",
        whitespace="to",
        numbers="cvbnm,",
        other="65;",
    )
    yield pool
