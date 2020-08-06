import math

import pytest

from password_validation.calculate import Classifier
from password_validation.calculate import EntropyRange
from password_validation.calculate import calculate_entropy
from password_validation.exceptions import UnacceptableCharacters, ClassificationError


def test_calculate_entropy_strict():
    password = "hello world"

    entropy = calculate_entropy(password, method="strict")
    assert entropy == math.log(len(set(password)) ** len(password), 2)


def test_calculate_entropy_normal():
    password = "hello world"

    entropy = calculate_entropy(password)
    assert entropy == math.log(27 ** len(password), 2)

    entropy = calculate_entropy(password, method="normal")
    assert entropy == math.log(27 ** len(password), 2)


def test_calculate_entropy_lenient():
    password = "hello world"
    entropy = calculate_entropy(password, method="lenient")
    assert entropy == math.log(95 ** len(password), 2)


def test_calculate_entropy_with_unacceptable_characters():
    password = "héllo world"
    with pytest.raises(UnacceptableCharacters):
        calculate_entropy(password)


def test_classifier():
    classifier = Classifier

    assert classifier
    assert classifier.default_ranges == {
        "Very Weak": EntropyRange(0, 28),
        "Weak": EntropyRange(28, 35),
        "Ok": EntropyRange(35, 59),
        "Good": EntropyRange(59, 127),
        "Very Good": EntropyRange(127, None),
    }

    classifier = Classifier()
    assert classifier.default_ranges == classifier.ranges


def test_classifier_classify():
    classifier = Classifier()

    assert classifier.classify(1) == "Very Weak"
    assert classifier.classify(28) == "Very Weak"
    assert classifier.classify(30) == "Weak"
    assert classifier.classify(35) == "Weak"
    assert classifier.classify(50) == "Ok"
    assert classifier.classify(59) == "Ok"
    assert classifier.classify(100) == "Good"
    assert classifier.classify(127) == "Good"
    assert classifier.classify(128) == "Very Good"
    assert classifier.classify(10000) == "Very Good"


def test_custom_classifier():
    ranges = {
        "Bad": EntropyRange(0, 500),
        "OK": EntropyRange(50, 100),
        "Good": EntropyRange(100, 150),
    }
    classifier = Classifier(ranges)


