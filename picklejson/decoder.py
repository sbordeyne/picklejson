from json import JSONDecoder
from typing import Any
import warnings

from packaging.version import Version

from picklejson import __version__
from picklejson.interfaces import JSONType
from picklejson.context import Context


class Decoder(JSONDecoder):
    def __init__(
        self, *, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, strict=True,
        object_pairs_hook=None, scope: dict[str, Any] | None = None,
    ):
        self.scope = scope
        if self.scope is None:
            self.scope = Context()
        self.passed_object_hook = object_hook or (lambda x: x)
        super().__init__(
            object_hook=self._object_hook, parse_float=parse_float,
            parse_int=parse_int, parse_constant=parse_constant,
            strict=strict, object_pairs_hook=object_pairs_hook
        )

    def _object_hook(self, decoded: JSONType):
        if not isinstance(decoded, dict):
            return self.passed_object_hook(decoded)

        if decoded.get('encoder_version') is None:
            return self.passed_object_hook(decoded)

        encoder_version = Version(decoded['encoder_version'])
        current_version = Version(__version__)
        if encoder_version.major != current_version.major:
            raise TypeError((
                f'Object was encoded with picklejson v{str(encoder_version)}. '
                f'Cannot decode with v{__version__}'
            ))

        if encoder_version.minor != current_version.minor:
            warnings.warn(
                (
                    f'Object was encoded with picklejson v{str(encoder_version)}. '
                    f'Current version is v{__version__}'
                ), UserWarning
            )

        # Get class from globals
        if self.scope is Context():
            scope_name = f"{decoded['name']}.{decoded['version']}"
        else:
            scope_name = decoded['name']
        klass = self.scope.get(scope_name)
        if klass is None:
            raise NameError((
                f'Object {scope_name} cannot be found in the global scope. '
                f'Has it been renamed?'
            ))

        # Instanciate the object anew and sets its attributes to what they were
        obj = klass(*decoded['init_args'], **decoded['init_kwargs'])
        for key, value in decoded['vars'].items():
            value = self._object_hook(value)
            obj_value = getattr(obj, key, None)
            if obj_value is None or obj_value != value:
                setattr(obj, key, value)

        return self.passed_object_hook(obj)
