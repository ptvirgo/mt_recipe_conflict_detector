# -*- coding: utf-8 -*-


class CraftItem(object):

    def __init__(self, name):

        if type(name) is not str:
            raise ValueError("name must be a str")

        if name[0] == ":":
            self.name = name[1:]
        else:
            self.name = name


class Group(object):

    def __init__(self, name, craft_items=None):

        if type(name) is not str:
            raise ValueError("name must be str")

        if craft_items is not None and type(craft_items) is not set:
            raise ValueError("craft_items must be a set of CraftItems")

        self.name = name
        self.craft_items = craft_items
