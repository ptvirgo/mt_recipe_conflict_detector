# -*- coding: utf-8 -*-

from . import helpers


class Craft(object):

    def __init__(self, output, recipe):

        if type(output) is not str:
            raise ValueError("output must be a str")

        if type(recipe) is not Recipe:
            raise ValueError("recipe must be a Recipe")

        self.output = output
        self.recipe = recipe

    def __repr__(self):
        return "<Craft output=%s>" % \
               (self.output,)


    @staticmethod
    def from_dict(data):
        r = Recipe.from_dict(data)
        c = Craft(data["output"], r)
        return c


class Recipe(object):

    def __init__(self, craft_items, craft_type="shaped"):

        if type(craft_items) is not list:
            raise ValueError("craft_items must be a list")

        if type(craft_type) is not str:
            raise ValueError("craft_type must be a str")

        self.craft_type = craft_type
        self.craft_items = craft_items 

    def __repr__(self):
        return "<Recipe craft_type=%s>" % \
               (self.craft_type,)

    @staticmethod
    def from_dict(data):

        if not "recipe" in data:
            raise ValueError("data must include recipe")
