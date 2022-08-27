# picklejson


[![PyPI](https://img.shields.io/pypi/v/picklejson.svg)](https://pypi.python.org/pypi/picklejson)
[![Documentation Status](https://readthedocs.org/projects/picklejson/badge/?version=latest)](https://readthedocs.org/projects/picklejson/badge/?version=latest)


Library that allows you to serialize any python object into JSON


* Free software: MIT license
* Documentation: https://picklejson.readthedocs.io.


## Usage

```python
from picklejson import JSONEncoder, JSONDecoder, serializable


@serializable
class Spam:
    def __init__(self, eggs: int):
        self.eggs = eggs


print(JSONEncoder().encode(Spam(1)))
# {"encoder_version": "1.0.0", "name": "Spam", "vars": {"eggs": 1}, "version": "1.0.0", "init_args": [1], "init_kwargs": {}, "init_prototype": {"eggs": "int"}}
print(JSONDecoder(globals()).decode('''{"encoder_version": "1.0.0", "name": "Spam", "vars": {"eggs": 1}, "version": "1.0.0", "init_args": [1], "init_kwargs": {}, "init_prototype": {"eggs": "int"}}'''))
# <__main__.Spam object at 0x10278f6d0>

```
