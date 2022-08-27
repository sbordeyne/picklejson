import json

import pytest

from picklejson import JSONEncoder, __version__


def test_simple_serialize(Person):
    _Person = Person
    john = _Person('John Doe', 35)
    encoded = JSONEncoder().encode(john)
    raw = json.loads(encoded)
    assert raw['encoder_version'] == __version__
    assert raw['name'] == '_Person'
    assert raw['version'] == '1.0.0'
    assert all(x == y for x, y in zip(raw['init_args'], ['John Doe', 35]))
    assert len(raw['init_kwargs']) == 0


def test_circular_serialize(Person):
    _Person = Person
    children = [_Person('Jane Doe', 8, False), _Person('Jack Doe', 13)]
    john = _Person('John Doe', 35, children=children)
    encoded = JSONEncoder().encode(john)
    raw = json.loads(encoded)
    assert raw['encoder_version'] == __version__
    assert raw['name'] == '_Person'
    assert raw['version'] == '1.0.0'
    assert all(x == y for x, y in zip(raw['init_args'], ['John Doe', 35]))
    assert len(raw['init_kwargs']) == 1


def test_not_serializable(NotSerializable):
    obj = NotSerializable('obj')
    with pytest.raises(TypeError):
        JSONEncoder().encode(obj)
