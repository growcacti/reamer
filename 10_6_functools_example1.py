from functools import singledispatch

@singledispatch
def count_items(obj):
    type_name = type(obj).__name__
    assert False, "Unsupported type"

@count_items.register
def _(text: str):
    return len(text.split())

@count_items.register
def _(lst: list):
    return len(lst)

print(count_items("This is a test"))  # Output: 4
print(count_items([1, 2, 3]))  # Output: 3
