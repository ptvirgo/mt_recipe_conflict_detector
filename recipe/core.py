# -*- coding: utf-8 -*-
"""Lingo / Data definitions

A CraftItem is a string representation of a single, specific item as can be
used in the Minetest inventory or craft table.
None or an empty string can represent a CraftItem
Validators should convert empty strings to None
CraftItems may appear with a leading ":", which should be removed for our
purposes.

Examples: "default:steel_ingot" or "default:diamond"

A GroupName is a string representation of a named collection of Minetest
Craftitems. 
The string must lead with the characters "group:"
Examples: "group:stick" or "group:wood"

A Group is a python set of CraftItems
Groups should not contain the empty string or None
Groups should reflect the set of Items expected per their related GroupName
Example: {"default:steel_ingot, "default:diamond"}

An Item can be a CraftItem, Group, or None. It may not be GroupName.

A RecipeCollection may be:
    - an Item
    - a list of up to 9 Items
    - a list containing up to 3 lists of up to 3 items, ie:
      [[Item, Item, Item], [Item, Item, Item], [Item, Item, Item]]

A CraftType is a string representing the "kind" of a given Recipe, per the
Minetest game. 
"shaped", "unshaped", "fuel", and "cooking" are standard.
"shaped" is the default.
Other CraftType strings may be introduced by Minetest mods.

Objects
-------
"""

from . import helpers

class Recipe(object):

    def __init__(self, recipe_collection, craft_type="shaped"):
        """Recipes combine a RecipeCollection and a named CraftType."""

        if type(craft_type) is not str:
            raise ValueError("craft_type must be str")

        self.craft_type = craft_type
        self.items = recipe_collection

    def _validate_collection(self, collection):
        """Return the recipe collection if valid, raise a ValueError
        otherwise
        """

        def validate_craftitem_name(x):
            """Validate a single CraftItem string"""
            if x == "": return

            if x[:6] == "group:":
                raise ValueError("Groupname '%s' shoud have been a Group (set)"
                                 % (x,))
            return x

        def validator(x):
            """Validate a single Item"""

            if x is None:
                return

            if type(x) is set:

                for s in x:
                    if validate_craftitem_name(s) is None:
                        raise ValueError("Groups cannot include empty CraftItem")
                return x

            if type(x) is str:
                return validate_craftitem_name(x)

class Craft(object):
    """A Craft is the combination of the CraftItem output of a Recipe, and the
Recipe itself.
    The Craft is distinct from the Recipe because two Recipes may be defined
identically (or in a conflicting way) with different outputs.  Distinguishing
the outputs allows that equality for Recipes is not dependent on equality of
Craft outputs.
    """

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
