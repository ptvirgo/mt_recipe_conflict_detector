# -*- coding: utf-8 -*-

# Copyright 2018 Pablo Virgo.

# This file is part of mt_recipe_conflict_detector.

# mt_recipe_conflict_detector is free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mt_recipe_conflict_detector is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mt_recipe_conflict_detector.
# If not, see <http://www.gnu.org/licenses/>.


def item_name(name):
    """Item names may lead with colons.  Drop 'em"""
    if name[0] == ":":
        name = name[1:]
    return name.split(" ")[0]


def group_name(name):
    """Group names may require adjustment"""

    if name[:6] == "group:":
        newname = name[6:]
    else:
        newname = name

    return newname.split(":")[-1]


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
