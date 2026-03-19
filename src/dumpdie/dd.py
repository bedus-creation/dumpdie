import os
import sys
import traceback
import types
from datetime import date, datetime
from decimal import Decimal
from inspect import getmembers, ismethod


def print_comment(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[0;38;5;247m'
    reset = '\033[0m'
    print(space + color + val + color+reset, end=end)


def print_property(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[m'
    print(space + color + val + color, end=end)


def print_const(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[1;038;5;208m'
    reset = '\033[0m'
    print(space + color + val + color + reset, end=end)


def print_string(val: str | bytes, space=0, end='\n', wrap: bool = True):
    space = space * 1 * ' '
    if isinstance(val, bytes):
        val = val.decode('utf-8', errors='replace')
    else:
        val = str(val)
    val = val.encode('utf-8', errors='replace').decode('utf-8')
    quote = '\033[038;5;208m"' if wrap else ''
    val = '\033[0;38;5;113m' + val + '\033[m'
    print(space + quote + val + quote, end=end)


def print_key(val, space: int = 0, end='\n'):
    space = space * ' '
    val = '\033[1;38;5;38m' + str(val) + '\033[m'
    print(space + val, end=end)


def print_dd_info():
    frame = None
    for current_frame in reversed(traceback.extract_stack()):
        if "dd.py" not in current_frame.filename:
            frame = current_frame
            break
    if not frame:
        return
    filename = frame.filename
    lineno = frame.lineno
    print_comment(f' // {filename}:{str(lineno)}', 0, '\n')


def print_var(val, space=0, indent: int = 0, end='', depth=0, visited=None):
    if visited is None:
        visited = set()

    depth = depth + 1
    if depth > 15:
        print_string("...", space, os.linesep)
        return

    # Tracking visited objects to prevent circular references (only for objects that are NOT primitives)
    if not isinstance(val, (int, float, str, bytes, bool, type(None), date, datetime, Decimal)):
        if id(val) in visited:
            print_comment(f"*recursion* {type(val).__name__}", space, os.linesep)
            return
        visited.add(id(val))

    match val:
        case types.ModuleType():
            print_string(str(val), space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case type():
            print_string(str(val), space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case types.FunctionType() | types.MethodType() | types.BuiltinFunctionType() | types.BuiltinMethodType():
            print_string(str(val), space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case Exception():
            print_string(f"{type(val).__name__}: {str(val)}", space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case int():
            print_key(val, space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case str():
            print_string(val, space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case bytes():
            print_string(val, space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case dict():
            print_dict(val, space, indent, depth=depth, visited=visited)
        case list():
            print_list(val, space, indent, depth=depth, visited=visited)
        case tuple():
            print_list(val, space, indent, depth=depth, visited=visited)
        case float():
            print_key(val, indent * 2, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case None:
            print_const('None', space, end=end)
        case date():
            print_key(val.strftime("%Y-%m-%d"), indent * 2, end=end)
        case datetime():
            print_key(val.strftime("%Y-%m-%d %H:%M:%S"), indent * 2, end=end)
        case Decimal():
            print_key(str(val), indent * 2, end=end)
            print_dd_info() if indent == 0 else print('', end=end)
        case object():
            print_object(val, indent, depth=depth, visited=visited)


def print_object(val, indent: int = 0, depth: int = 0, visited=None):
    class_name = type(val).__name__
    print_string(class_name, space=min(1, indent), end='', wrap=False)
    print_const('^', space=0, end='')

    # Safely get members, handling objects without __dict__ (like Decimal or those with __slots__)
    members = {}
    if hasattr(val, '__dict__'):
        for n, m in val.__dict__.items():
            try:
                if not callable(m) and not ismethod(m):
                    members[n] = m
            except Exception:
                continue
    else:
        # Fallback to getmembers if __dict__ is missing, filtering out internals and methods
        try:
            for n, m in getmembers(val):
                try:
                    if not n.startswith('__') and not callable(m) and not ismethod(m):
                        members[n] = m
                except Exception:
                    continue
        except Exception:
            pass

    if not members and indent > 0:
        print_const('{}', space=1, end='\n')
        return

    print_const('{', space=1, end='')
    # print_comment('#' + hex(id(val)), space=0, end='\n')
    print_dd_info() if indent == 0 else print('', end='\n')
    for _name, member in members.items():
        symbol = '+'
        if _name.startswith(f'_{class_name}'):
            symbol = '-'
            _name = _name.replace(f'_{class_name}', '')
        elif _name.startswith('_'):
            symbol = '#'
        print_const(symbol, indent * 2 + 2, end='')
        print_property(_name, 0, '')
        print_const(':', 0)
        print_var(member, 1, indent=indent + 1, end='\n', depth=depth, visited=visited)

    print_const('}', space=indent * 2, end='\n')


def print_list(val: list | tuple, space: int = 0, indent: int = 0, depth: int = 0, visited=None):
    print_string(type(val).__name__ + ':' + str(len(val)), space=min(1, indent), end='', wrap=False)
    if len(val) == 0 and indent > 0:
        print_const(' []', space=0, end='\n')
        return

    print_const('[', space=1, end='')
    print_dd_info() if indent == 0 else print('', end='\n')
    for item in range(len(val)):
        value = val[item]
        print_key(item, indent * 2 + 2, '')
        print_const('=>', 1)
        print_var(value, 1, indent=indent + 1, end='\n', depth=depth, visited=visited)
    print_const(']', space=indent * 2, end='\n')


def print_dict(val: dict, space=0, indent: int = 0, depth: int = 0, visited=None):
    print_string(type(val).__name__, space=min(1, indent), end='', wrap=False)
    if len(val) == 0 and indent > 0:
        print_const('{}', space=1, end='\n')
        return

    print_const('{', space=1, end='')

    if indent == 0:
        print_dd_info()
    else:
        print('', end='\n')

    for key, value in val.items():
        print_string(key, indent * 2 + 2, end='')
        print_const(':', 0)
        print_var(value, 1, indent=indent + 1, end='\n', depth=depth, visited=visited)
    print_const('}', space=indent * 2, end='\n')


def dd(*args):
    for arg in args:
        print_var(arg)

    sys.exit("")

def dump(*args):
    for arg in args:
        print_var(arg)
