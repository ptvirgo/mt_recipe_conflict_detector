# -*- coding: utf-8 -*-


def item_name(name):
    """Item names may lead with colons.  Drop 'em"""
    if name[0] == ":":
        return name[1:]
    else:
        return name


def map_recipe_collection(f, item):
    """Provides a recursive map function that can cover the expected
    RecipeCollection structure
    """
    if item is None:
        return

    if type(item) is not list:
        return f(item)

    return [map_recipe_collection(f, i) for i in item]


def reduce_recipe_collection(f, item, initial):
    """Provides a reduce (fold) function that can cover the expected
    RecipeCollection structure
    """
    if item is None:
        return initial

    if type(item) is not list:
        return f(initial, item)

    value = initial
    for i in item:
        value = reduce_recipe_collection(f, i, value)

    return value


def items_conflict(a, b):
    """Return True if the provided CraftItems conflict"""

    if type(a) is type(b):
        return a == b

    if type(a) is set:
        return items_conflict(b, a)

    if a in b:
        return True
