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

    if type(item) is not list:
        return f(item)

    return [map_recipe_collection(f, i) for i in item]


def reduce_recipe_collection(f, item, initial):
    """Provides a reduce (fold) function that can cover the expected
    RecipeCollection structure
    """

    if type(item) is not list:
        return f(initial, item)

    value = initial
    for i in item:
        value = reduce_recipe_collection(f, i, value)

    return value


def items_match(a, b):
    """Return True if the provided CraftItems match"""

    if type(a) is type(b):
        return a == b

    if type(a) is set:
        return items_match(b, a)

    if type(a) is str and type(b) is set:
        return a in b

    return False
