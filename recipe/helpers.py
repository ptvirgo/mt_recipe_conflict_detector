# -*- coding: utf-8 -*-

from .item import CraftItem, Group


def item_or_group(name):
    """Given the name of a recipe item (per the minetest recipe exporter),
    return the appropriate CraftItem or Group
    """
    
    if name[:6] == "group:":
       return Group(name[6:])
    else:
       return CraftItem(name)
