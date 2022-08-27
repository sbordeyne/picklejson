from json import JSONEncoder
from typing import Any

from picklejson import __version__
from picklejson.interfaces import JSONType


class Encoder(JSONEncoder):
    def default(self, obj: Any) -> JSONType:
        if isinstance(obj, JSONType):
            return obj

        if isinstance(obj, type):
            return obj.__name__

        if not getattr(obj, '__serializable__', False):
            # Object should be marked as serializable
            return super().default(obj)

        output: dict[str, JSONType] = {}
        output['encoder_version'] = __version__
        output['name'] = obj.__class__.__name__
        output['vars'] = {k: self.default(v) for k, v in vars(obj).items()}
        output['version'] = obj.__version__
        output['init_args'] = [self.default(a) for a in obj.__init_args__]
        output['init_kwargs'] = {k: self.default(v) for k, v in obj.__init_kwargs__.items()}
        output['init_prototype'] = {
            k: self.default(v)
            for k, v in obj.__init__.__annotations__.items()
        }
        return output
