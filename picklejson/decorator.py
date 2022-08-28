from typing import Any, Callable

from picklejson.context import Context

# This complicated looking decorator does multiple things :
# First off, it marks the object as serializable by the module (attribute __serializable__)
# Then it sets the version of the serialization on the object
# It then replaces the object's initializer with a custom function to register the
# arguments passed as input to the initializer so that, when deserializing, the object
# can be recreated as it was.
# Finally, if the decorator is passed without arguments,
# it works as it should (setting the default version to 1.0.0)


def serializable(object_version: str | tuple[int | str] | Callable) -> type:
    '''Marks a python object as serializable.'''
    if isinstance(object_version, tuple | list):
        object_version = '.'.join(str(v) for v in object_version)
    context: Context = Context()

    def _serializable(klass: type) -> type:
        klass.__serializable__ = True
        klass.__version__ = object_version if isinstance(object_version, str) else '1.0.0'
        context[f'{klass.__name__}.{klass.__version__}'] = klass

        def initializer(*args: tuple[Any], **kwargs: dict[str, Any]) -> Callable:
            nonlocal klass
            self, *args = args
            self.__init_args__ = tuple(args)
            self.__init_kwargs__ = {k: v for k, v in kwargs.items()}
            return klass.__original_initializer__(self, *args, **kwargs)
        initializer.__annotations__ = klass.__init__.__annotations__
        initializer.__doc__ = klass.__init__.__doc__
        klass.__original_initializer__ = klass.__init__
        klass.__init__ = initializer
        return klass

    if callable(object_version):
        return _serializable(object_version)
    return _serializable
