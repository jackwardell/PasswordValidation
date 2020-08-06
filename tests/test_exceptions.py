import pytest

from password_validation.exceptions import UnacceptableCharacters, ClassificationError


def test_unacceptable_characters():
    assert issubclass(UnacceptableCharacters, Exception)
    assert UnacceptableCharacters

    with pytest.raises(UnacceptableCharacters):
        raise UnacceptableCharacters()

    unacceptable_characters = UnacceptableCharacters()
    assert unacceptable_characters
    assert isinstance(unacceptable_characters, UnacceptableCharacters)

    with pytest.raises(UnacceptableCharacters):
        raise unacceptable_characters


def test_unacceptable_characters():
    assert issubclass(ClassificationError, Exception)
    assert ClassificationError

    with pytest.raises(ClassificationError):
        raise ClassificationError()

    classification_error = ClassificationError()
    assert classification_error
    assert isinstance(classification_error, ClassificationError)

    with pytest.raises(ClassificationError):
        raise classification_error
