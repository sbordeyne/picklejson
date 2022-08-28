'''
Library that allows you to serialize any python object into JSON
'''
__version__ = '1.1.0'

from picklejson.decoder import Decoder as JSONDecoder  # noqa
from picklejson.encoder import Encoder as JSONEncoder  # noqa
from picklejson.interfaces import JSONType  # noqa
from picklejson.decorator import serializable  # noqa
from picklejson.functions import dump, dumps, load, loads  # noqa
from picklejson.context import Context  # noqa
