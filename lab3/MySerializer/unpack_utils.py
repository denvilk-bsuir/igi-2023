import inspect
import builtins
import types
from MySerializer.constants import PRIMITIVES
from types import FunctionType, LambdaType, CodeType, CellType, GeneratorType, ModuleType

def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)


def is_iterable(obj):
    return getattr(obj, "__iter__", None) is not None

def unpack(src):
    if isinstance(src, PRIMITIVES):
        return src

    elif isinstance(src, dict):
        if "function" in src.values():
            return unpack_function(src)

        elif "object" in src.values():
            return unpack_object(src)

        elif "class" in src.values():
            return unpack_class(src)
        
        elif "code" in src.values():
            return unpack_code(src)
        
        elif "iterator" in src.values():
            return unpack_iterator(src)

        else:
            return unpack_iterable(src)

    elif is_iterable(src):
        return unpack_iterable(src)

    elif "module" == src.__class__.__name__:
        return unpack_module(src)

    else:

        raise Exception("Unknown type")

def unpack_module(obj):
    return obj

def unpack_class(obj):
    class_bases = tuple(unpack_class(base) for base in obj["__bases__"])
    class_methods = {}

    for attr, value in obj.items():
        class_methods[attr] = unpack(value)

    result = type(obj["__name__"], class_bases, class_methods)

    for key, method in class_methods.items():
        if inspect.isfunction(method):
            method.__globals__.update({result.__name__: result})

    return result

def unpack_iterator(obj):
    for i in unpack(obj["__values__"]):
        yield i

def unpack_code(obj):
    attrs = {}

    for key, value in obj.items():
        attrs[key] = unpack(value)

    result = CodeType(attrs['co_argcount'],
                     attrs['co_posonlyargcount'],
                     attrs['co_kwonlyargcount'],
                     attrs['co_nlocals'],
                     attrs['co_stacksize'],
                     attrs['co_flags'],
                     bytes(attrs['co_code']),
                     tuple(unpack(attrs['co_consts'])),
                     tuple(attrs['co_names']),
                     tuple(attrs['co_varnames']),
                     attrs['co_filename'],
                     attrs['co_name'],
                     attrs['co_firstlineno'],
                     bytes(attrs['co_lnotab']),
                     tuple(attrs['co_freevars']),
                     tuple(attrs['co_cellvars']))

    return result

def unpack_object(obj):
    obj_class = unpack(obj["__class__"])
    attrs = {}

    for key, value in obj["attr"].items():
        attrs[key] = unpack(value)

    if "property" in obj_class.__name__:
        obj_class = property
        result = property(fget=attrs["fget"],fset=attrs["fset"],fdel=attrs["fdel"])
    elif "cell" in obj_class.__name__:
        result = CellType(attrs["cell_contents"])
    else:
        result = object.__new__(obj_class)
        result.__dict__ = attrs

    return result

def unpack_function(src):
    arguments = src["__args__"]
    globs = src["__globals__"]
    globs["__builtins__"] = __builtins__

    for key in src["__globals__"]:
        if key in arguments["co_names"]:
            try:
                globs[key] = __import__(src["__globals__"][key])

            except:
                if globs[key] != src["__name__"]:
                    globs[key] = unpack(src["__globals__"][key])


    coded = CodeType(arguments['co_argcount'],
                     arguments['co_posonlyargcount'],
                     arguments['co_kwonlyargcount'],
                     arguments['co_nlocals'],
                     arguments['co_stacksize'],
                     arguments['co_flags'],
                     bytes(arguments['co_code']),
                     tuple(arguments['co_consts']),
                     tuple(arguments['co_names']),
                     tuple(arguments['co_varnames']),
                     arguments['co_filename'],
                     arguments['co_name'],
                     arguments['co_firstlineno'],
                     bytes(arguments['co_lnotab']),
                     tuple(arguments['co_freevars']),
                     tuple(arguments['co_cellvars']))

    func_result = FunctionType(coded, globs, closure = unpack(src["__closure__"]))
    func_result.__globals__.update({func_result.__name__: func_result})

    return func_result


def unpack_iterable(obj):
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        unpacked_iterable = []

        for value in obj:
            unpacked_iterable.append(unpack(value))

        if isinstance(obj, tuple):
            return tuple(unpacked_iterable)

        if isinstance(obj, set):
            return set(unpacked_iterable)

        return unpacked_iterable

    elif isinstance(obj, dict):
        unpacked_dict = {}

        for key, value in obj.items():
            unpacked_dict[key] = unpack(value)

        return unpacked_dict


def turn_obj_into_dict(obj):
    if isinstance(obj, type(None)):

        return {
            "None": "None"
        }

    elif isinstance(obj, PRIMITIVE_TYPES):

        return {
            str(type(obj)): obj
        }

    elif isinstance(obj, (list, tuple, set)):
        result = []

        for item in obj:
            result.append(turn_obj_into_dict(item))

        return {
            str(type(obj)): result
        }

    elif isinstance(obj, dict):
        result = {}

        for key, value in obj.items():
            result[key] = turn_obj_into_dict(value)

        return result

    else:
        raise Exception("Unknown type")


def restore_object_from_dict(src):
    if type(src) is dict:

        if len(src.keys()) == 1:
            key, value = list(src.items())[0]

            if key == "None":
                return None

            elif isinstance(value, PRIMITIVE_TYPES):
                return value

            elif isinstance(value, list):
                result = []

                for obj in value:
                    result.append(restore_object_from_dict(obj))

                if key == "<class 'tuple'>":
                    result = tuple(result)

                elif key == "<class 'set'>":
                    result = set(result)

                return result

        result = {}

        for key, val in src.items():
            result[key] = restore_object_from_dict(val)

        return result

    else:
        raise Exception("Object type must be dict")