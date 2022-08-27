import json

import pytest

from picklejson import JSONDecoder


def test_simple_deserialize(Person, simple_encoded: str):
    decoded = JSONDecoder({'_Person': Person}).decode(simple_encoded)
    assert isinstance(decoded, Person)
    assert decoded.name == 'John Doe'
    assert decoded.age == 35
    assert decoded.is_male is True
    assert len(decoded.children) == 0


def test_circular_deserialize(Person):
    encoded = (
        '{"encoder_version": "1.0.0", "name": "_Person", "vars": '
        '{"__init_args__": ["John Doe", 35], "__init_kwargs__": '
        '{"children": [{"encoder_version": "1.0.0", "name": "_Person", '
        '"vars": {"__init_args__": ["Jane Doe", 8, false], "__init_kwargs__": '
        '{}, "name": "Jane Doe", "age": 8, "is_male": false, "children": []}, '
        '"version": "1.0.0", "init_args": ["Jane Doe", 8, false], '
        '"init_kwargs": {}, "init_prototype": {"name": "str", "age": "int", '
        '"is_male": "bool", "children": "list"}}, {"encoder_version": "1.0.0", '
        '"name": "_Person", "vars": {"__init_args__": ["Jack Doe", 13], '
        '"__init_kwargs__": {}, "name": "Jack Doe", "age": 13, "is_male": true, '
        '"children": []}, "version": "1.0.0", "init_args": ["Jack Doe", 13], '
        '"init_kwargs": {}, "init_prototype": {"name": "str", "age": "int", '
        '"is_male": "bool", "children": "list"}}]}, "name": "John Doe", '
        '"age": 35, "is_male": true, "children": [{"encoder_version": "1.0.0",'
        ' "name": "_Person", "vars": {"__init_args__": ["Jane Doe", 8, false], '
        '"__init_kwargs__": {}, "name": "Jane Doe", "age": 8, "is_male": false, '
        '"children": []}, "version": "1.0.0", "init_args": ["Jane Doe", 8, false], '
        '"init_kwargs": {}, "init_prototype": {"name": "str", "age": "int", '
        '"is_male": "bool", "children": "list"}}, {"encoder_version": "1.0.0", '
        '"name": "_Person", "vars": {"__init_args__": ["Jack Doe", 13], '
        '"__init_kwargs__": {}, "name": "Jack Doe", "age": 13, "is_male": true, '
        '"children": []}, "version": "1.0.0", "init_args": ["Jack Doe", 13], '
        '"init_kwargs": {}, "init_prototype": {"name": "str", "age": "int", '
        '"is_male": "bool", "children": "list"}}]}, "version": "1.0.0", "init_args": '
        '["John Doe", 35], "init_kwargs": {"children": [{"encoder_version": '
        '"1.0.0", "name": "_Person", "vars": {"__init_args__": ["Jane Doe", 8, false], '
        '"__init_kwargs__": {}, "name": "Jane Doe", "age": 8, "is_male": false, '
        '"children": []}, "version": "1.0.0", "init_args": ["Jane Doe", 8, false], '
        '"init_kwargs": {}, "init_prototype": {"name": "str", "age": "int", "is_male": '
        '"bool", "children": "list"}}, {"encoder_version": "1.0.0", "name": "_Person", '
        '"vars": {"__init_args__": ["Jack Doe", 13], "__init_kwargs__": {}, "name": '
        '"Jack Doe", "age": 13, "is_male": true, "children": []}, "version": "1.0.0", '
        '"init_args": ["Jack Doe", 13], "init_kwargs": {}, "init_prototype": {"name": '
        '"str", "age": "int", "is_male": "bool", "children": "list"}}]}, '
        '"init_prototype": {"name": "str", "age": "int", "is_male": "bool", '
        '"children": "list"}}'
    )
    decoded = JSONDecoder({'_Person': Person}).decode(encoded)
    assert isinstance(decoded, Person)
    assert decoded.name == 'John Doe'
    assert decoded.age == 35
    assert decoded.is_male is True
    assert len(decoded.children) == 2
    assert all(isinstance(child, Person) for child in decoded.children)


def test_unbound_deserialize(simple_encoded: str):
    with pytest.raises(NameError):
        JSONDecoder({}).decode(simple_encoded)


def test_version_deserialize(Person, simple_encoded: str):
    raw_json = json.loads(simple_encoded)
    raw_json['encoder_version'] = '2.0.0'
    encoded_v2 = json.dumps(raw_json)
    raw_json['encoder_version'] = '1.1.0'
    encoded_warn = json.dumps(raw_json)

    with pytest.raises(TypeError):
        JSONDecoder({'_Person': Person}).decode(encoded_v2)

    with pytest.warns(UserWarning):
        JSONDecoder({'_Person': Person}).decode(encoded_warn)
