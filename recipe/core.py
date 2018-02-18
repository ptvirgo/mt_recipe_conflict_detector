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

    def ingredients(self, update=False):
        """Return a flat list of the Items (excluding None) for this Recipe.
        As side effect, stores the ingredient list if it has not already been
stored or if the update argument is True
        """
        if update or not hasattr(self, "_ingredients"):
            self._ingredients = helpers.reduce_recipe_collection(
                (lambda a, b: a + [b]), self.items, [])

        return list(self._ingredients)

    def conflicts(self, other):
        """Recipe detects conflicts with other Recipes"""

        def cut_match(item, collection):
            """If an Item can be matched in a collection of Items, return the 
            collection minus the first match.  Return false if the item can't be
            matched.
            """
            for i in range(len(collection)):
                if helpers.items_match(item, collection[i]):
                    return collection[:i] + collection[i+1:]
            return False

        # usually, craft types must match in order to conflict
        if self.craft_type != "shaped" and other.craft_type != "shaped":

            if self.craft_type != other.craft_type:
                return False

            these_items = self.ingredients()
            those_items = other.ingredients()

            for item in these_items:
                those_items = cut_match(item, those_items)

                if those_items is False:
                    return False

            return those_items == []

        raise NotImplementedError("Incomplete conflict resolution.  Dead.")

    def unshaped_conflict(self, other):
        """Detect conflicts for Recipes without shape restrictions"""
        

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
