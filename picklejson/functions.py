import io
import json
from typing import Any, Callable

from picklejson.encoder import JSONEncoder
from picklejson.decoder import JSONDecoder
from picklejson.interfaces import JSONType


__all__ = ('load', 'loads', 'dump', 'dumps')


def _make_doc(f: Callable[..., str | None]):
    name = f.__name__
    jsonfunc = getattr(json, name)
    f.__doc__ = jsonfunc.__doc__
    return f


@_make_doc
def load(
    fp: io.FileIO, *, object_hook: Callable[[dict], Any] | None = None,
    parse_float: Callable[[str], float] | None = None,
    parse_int: Callable[[str], int] | None = None,
    parse_constant: Callable[[str], str] | None = None,
    object_pairs_hook: Callable[[tuple[JSONType, JSONType]], Any] | None = None,
    **kw
):
    return json.load(
        fp, cls=JSONDecoder, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook
    )


@_make_doc
def loads(
    s: str, *, object_hook: Callable[[dict], Any] | None = None,
    parse_float: Callable[[str], float] | None = None,
    parse_int: Callable[[str], int] | None = None,
    parse_constant: Callable[[str], str] | None = None,
    object_pairs_hook: Callable[[tuple[JSONType, JSONType]], Any] | None = None,
    **kw
):
    return json.loads(
        s, cls=JSONDecoder, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook
    )


@_make_doc
def dump(
    obj: Any, fp: io.FileIO, *, skipkeys: bool = False,
    ensure_ascii: bool = True, check_circular: bool = True,
    allow_nan: bool = True, indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], JSONType] = None,
    sort_keys: bool = False, **kw
):
    return json.dump(
        obj, fp, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan,
        indent=indent, separators=separators, default=default,
        sort_keys=sort_keys, cls=JSONEncoder,
    )


@_make_doc
def dumps(
    obj: Any, *, skipkeys: bool = False,
    ensure_ascii: bool = True, check_circular: bool = True,
    allow_nan: bool = True, indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], JSONType] = None,
    sort_keys: bool = False, **kw
):
    return json.dumps(
        obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan,
        indent=indent, separators=separators, default=default,
        sort_keys=sort_keys, cls=JSONEncoder,
    )
