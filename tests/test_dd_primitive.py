from datetime import date, datetime
from decimal import Decimal

from dumpdie.dd import dump


def test_answer():
    assert 1 == 1

def test_dd_everything():
    data = {
        "int": 42,
        "str": "hello",
        "bytes": b"world",
        "float": 3.14,
        "bool": True,
        "none": None,
        "date": date(2024, 1, 1),
        "datetime": datetime(2024, 1, 1, 12, 0, 0),
        "decimal": Decimal("10.50"),
        "exception": ValueError("Something went wrong"),
        "list": [1, "two", b"three"],
        "tuple": (4, 5, 6),
        "nested": {
            "a": 1,
            "b": [2, 3]
        }
    }
    dump(data, 1)

def test_dd_exception():
    try:
        raise TypeError("Unexpected type found")
    except Exception as e:
        dump(e)

def test_dd_stacktrace():
    import traceback
    try:
        raise RuntimeError("A catastrophic failure")
    except Exception:
        stack = traceback
        dump(stack)

class Author:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

def test_dd_nested_relationship():
    author = Author("J.K. Rowling")
    book = Book("Harry Potter", author)
    data = {
        "book": book,
        "metadata": {
            "tags": ["fantasy", "magic"],
            "related_authors": [author]
        }
    }
    dump(data)
