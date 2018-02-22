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
        Side effects: Cache the result and set self._sortable
        """
        def redux(base, item):

            if item is None:
                return base

            if type(item) is set:
                base["groups"].append(item)
                return base

            if type(item) is str:
                base["craft_items"].append(item)
                return base

        if update or not hasattr(self, "_ingredients"):
            ingredients = helpers.reduce_recipe_collection(
                redux, self.items, {"craft_items": [], "groups": []})
            ingredients["craft_items"] = sorted(ingredients["craft_items"])
            self._ingredients = ingredients

        # Returning a fresh dict in order to prevent mutation of the cached
        # object
        return {"craft_items": list(self._ingredients["craft_items"]),
                "groups": list(self._ingredients["groups"])}

    def sortable(self, update=False):
        """Is this Recipe sortable?  Side effects may include caching the
        result and _ingredients."""

        if update or not hasattr(self, "_sortable"):
            ingredients = self.ingredients(True)
            self._sortable = self.craft_type != "shaped" and \
                ingredients["groups"] == []

        return self._sortable

    def conflicts(self, other):
        """Recipe detects conflicts with other Recipes"""

        if self.craft_type != "shaped" and other.craft_type != "shaped":
            # usually, craft types must match in order to conflict
            if self.craft_type == other.craft_type:
                return self._unshaped_match(other)
            else:
                return False

        elif self.craft_type == "shaped" and other.craft_type == "shaped":
            return self._shaped_match(other)

        else:
            return self._unshaped_match(other)

    @staticmethod
    def _cut_match(item, collection, sorted_collection=False):
        """Cut a given Item from a collection of Items.
        parameters:
            item - the Item to be cut
            collection - list of Items
            sorted_collection - bool indicating where a (possibly) more
                efficient search on an ordered list is appropriate
        returns:
            Bool indicating success, remains of the collection (unaltered if
            no match)
        """
        i = 0
        end = len(collection)

        while i < end:
            if helpers.items_match(item, collection[i]):
                return (True, collection[:i] + collection[i+1:])
            if sorted_collection and item > collection[i]:
                return (False, collection)
            i += 1

        return (False, collection)

    def _unshaped_match(self, other):
        """Given another Recipe, return a bool describing whether this and the
        other are effectively the same, discounting Item order and empty Items
        """

        these = self.ingredients()
        those = other.ingredients()
        for item in these["craft_items"]:
            found, remaining = self._cut_match(
                item, those["craft_items"], True)

            if found:
                those["craft_items"] = remaining
                continue

            found, remaining = self._cut_match(item, those["groups"])

            if found:
                those["groups"] = remaining
                continue

            return False

        for item in these["groups"]:
            found, remaining = self._cut_match(item, those["craft_items"])

            if found:
                those["craft_items"] = remaining
                continue

            found, remaining = self._cut_match(item, those["groups"])

            if found:
                those["groups"] = remaining
                continue

            return False

        return those["craft_items"] == [] and those["groups"] == []

    def _shaped_match(self, other):
        """Given another shaped Recipe, return a bool indicating whether this
        and the other conflict.
        """
        these, those = self._normalize(self.items, other.items)

        i = 0
        j = 0
        for i in range(len(these)):
            for j in range(len(these[i])):
                if not helpers.items_match(these[i][j], those[i][j]):
                    return False
        return True

    @staticmethod
    def _normalize(a, b):
        """Given two shaped item lists, return variations filled out with None
        as needed to match size and preserve possible matching
        """

        # Let's not mutate item lists
        items1 = list(a)
        items2 = list(b)

        def height(items):
            return len(items)

        def width(items):
            return max([len(row) for row in items])

        def get_top_offset(items):
            i = 0

            while i < height(items):
                for item in items[i]:
                    if item is not None:
                        return i
                i += 1
            return i

        def get_left_offset(items):
            i = 0

            while i < width(items):
                for row in items:
                    if row[i] is not None:
                        return i
                i += 1
            return i

        def fill_height(total, offset, items):
            new_row = [[None] * width(items)]

            while height(items) < total:
                if offset > 0:
                    items = new_row + items
                    offset -= 1
                else:
                    items = items + new_row

            return items

        def fill_width(total, offset, items):
            h = height(items)

            for i in range(h):
                missing = total - len(items[i])
                prefix = min(missing, offset)
                postfix = missing - prefix
                items[i] = [None] * prefix + items[i] + [None] * postfix

            return items

        expected_height = max(height(items1), height(items2))
        expected_width = max(width(items1), width(items2))

        items1 = fill_height(expected_height, get_top_offset(items2), items1)
        items1 = fill_width(expected_width, get_left_offset(items2), items1)

        items2 = fill_height(expected_height, get_top_offset(items1), items2)
        items2 = fill_width(expected_width, get_left_offset(items1), items2)

        return items1, items2


class Craft(object):
    """A Craft is the combination of the CraftItem output of a Recipe, and the
Recipe itself.
    The Craft is distinct from the Recipe because two Recipes may be defined
identically (or in a conflicting way) with different outputs.  Distinguishing
the outputs allows that equality for Recipes is not dependent on equality of
Craft outputs.
    """

    def __init__(self, recipe, output):

        if type(output) is not str:
            raise ValueError("output must be a str")

        if type(recipe) is not Recipe:
            raise ValueError("recipe must be a Recipe")

        self.output = output
        self.recipe = recipe

    def __repr__(self):
        return "<Craft output=%s>" % \
               (self.output,)
