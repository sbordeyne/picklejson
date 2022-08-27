import pytest

from picklejson import serializable


@serializable
class _Person:
    def __init__(self, name: str, age: int, is_male: bool = True, children: list['Person'] = None):
        self.name = name
        self.age = age
        self.is_male = is_male
        self.children = children or []


class _NotSerializable:
    def __init__(self, name: str):
        self.name = name


@pytest.fixture
def Person() -> type:
    return _Person


@pytest.fixture
def simple_encoded():
    return (
        '{"encoder_version": "1.0.0", "name": "_Person", '
        '"vars": {"__init_args__": ["John Doe", 35], "__init_kwargs__": {}, '
        '"name": "John Doe", "age": 35, "is_male": true, "children": []}, '
        '"version": "1.0.0", "init_args": ["John Doe", 35], "init_kwargs": {}, '
        '"init_prototype": {"name": "str", "age": "int", "is_male": "bool", '
        '"children": "list"}}'
    )

@pytest.fixture
def NotSerializable() -> type:
    return _NotSerializable
