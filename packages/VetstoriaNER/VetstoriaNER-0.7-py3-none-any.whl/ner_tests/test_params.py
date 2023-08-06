#importing the Entity_Recognizer class from the EntityRecognizer.py file 
import sys
import os
import pytest

from VetstoriaNER import EntityRecognizer

TEST_VALUES = [
    pytest.param('i have a cat',['cat']),
    pytest.param('we have a dog',['dog']),
    pytest.param('my name is abdul',None),
    pytest.param('k9',None),
    pytest.param('i am abdul and i currently work as an intern at vetstoria and my pet is a wonderful cat',['cat']),
    pytest.param('i have a cat and a dog',['cat', 'dog']),
    pytest.param('tiger',['tiger']),
    pytest.param('my pet is a fish',['fish']),
    pytest.param('',None),
    pytest.param('i have you',None),
    pytest.param('i have no idea',None)
]


@pytest.mark.parametrize("input,expected",TEST_VALUES)
def test_output(input,expected):
    entity_recognizer = EntityRecognizer('species-detection')
    identified_species_names = entity_recognizer.recognizeSpecies(input)
    assert identified_species_names == expected