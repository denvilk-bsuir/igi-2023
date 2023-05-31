import inspect
import types
from MySerializer.constants import PRIMITIVES, COLLECTIONS
from types import FunctionType, BuiltinFunctionType, LambdaType, GetSetDescriptorType, MappingProxyType, \
    MethodDescriptorType, WrapperDescriptorType


def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)


def is_iterable(obj):
    return getattr(obj, "__iter__", None) is not None


def pack(obj):
    if isinstance(obj, PRIMITIVES):
        return obj
    
    elif isinstance(obj, COLLECTIONS):
        return obj

    elif is_function(obj):
        return pack_function(obj)

    elif inspect.iscode(obj):
        return pack_code(obj)

    elif inspect.isclass(obj):
        return pack_class(obj)

    elif is_iterable(obj):
        return pack_iterable(obj)

    else:
        return pack_object(obj)


def pack_function(obj, cls=None):
    result = {"__type__": "function"}

    if inspect.ismethod(obj):
        obj = obj.__func__

    result["__name__"] = obj.__name__

    globs = get_global_vars(obj, cls)
    result["__globals__"] = pack_iterable(globs)
    result["__closure__"] = pack(obj.__closure__)

    
    arguments = {}

    for (key, value) in inspect.getmembers(obj.__code__):
        if key.startswith("co_"):
            if isinstance(value, bytes):
                value = list(value)

            if is_iterable(value) and not isinstance(value, str):
                packed_vals = []

                for val in value:
                    if val is not None:
                        packed_vals.append(pack(val))

                    else:
                        packed_vals.append(None)

                arguments[key] = packed_vals

                continue

            arguments[key] = value

    result["__args__"] = arguments

    return result


def get_global_vars(func, cls):
    globs = {}

    for global_var in func.__code__.co_names:
        if global_var in func.__globals__:
            if isinstance(func.__globals__[global_var], types.ModuleType):
                globs[global_var] = func.__globals__[global_var].__name__

            elif inspect.isclass(func.__globals__[global_var]):
                if cls and func.__globals__[global_var] != cls:
                    globs[global_var] = func.__globals__[global_var]

            elif global_var != func.__code__.co_name:
                globs[global_var] = func.__globals__[global_var]

            else:
                globs[global_var] = func.__name__
    return globs


def pack_iterable(obj):

    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, bytes):
        packed_iterable = []

        for value in obj:
            packed_iterable.append(pack(value))

        if isinstance(obj, tuple):
            return tuple(packed_iterable)

        if isinstance(obj, set):
            return set(packed_iterable)

        return packed_iterable

    elif isinstance(obj, dict):
        packed_dict = {}

        for key, value in obj.items():
            packed_dict[key] = pack(value)

        return packed_dict
    
    else:
        result = {"__type__": "iterator"}
        values = []
        for i in obj:
            values.append(pack(i))
        
        result["__values__"] = values

        return result


def pack_code(obj):   
    result = {"__type__":"code"}

    for key, value in inspect.getmembers(obj):
        if not key.startswith("co"):
            continue

        result[key] = pack(value)

    return result


def pack_class(obj):
    result = {'__type__': 'class', '__name__': obj.__name__}

    for attr in inspect.getmembers(obj):
        if attr[0] not in (
                "__mro__", "__base__", "__basicsize__",
                "__class__", "__dictoffset__", "__name__",
                "__qualname__", "__text_signature__", "__itemsize__",
                "__flags__", "__weakrefoffset__", "__objclass__"
        ) and type(attr[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
        ):
            attr_value = getattr(obj, attr[0])

            if is_function(attr_value):
                result[attr[0]] = pack_function(attr_value, obj)

            else:
                result[attr[0]] = pack(attr_value)

    result["__bases__"] = [pack_class(base) for base in obj.__bases__ if base != object]

    return result

def pack_object(obj):
    result = {"__type__": "object", "__class__": pack_class(obj.__class__), "attr": {}}
    if(obj.__class__.__name__ in ["property","cell"]):
        for key, value in inspect.getmembers(obj):
            if not key.startswith("__"):
                result["attr"][key] = pack(value)

    else:
        for key, value in inspect.getmembers(obj):
            if not key.startswith("__") and not is_function(value):
                result["attr"][key] = pack(value)

    return result
