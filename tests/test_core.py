#/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from recipe import Craft, Recipe


class TestRecipe(unittest.TestCase):

    metals = {"default:steel_ingot", "default:bronze_ingot",
              "default:gold_ingot"}
    woods = {"default:wood", "default:junglewood", "default:pine_wood"}

    def test_recipe_creation(self):
        """Recipes can be created with a basic RecipeCollection"""
        # One default:wood
        Recipe("default:wood", "fuel")

        # One item from a simple wood group
        Recipe({"default:wood", "default:pine_wood"}, "fuel")

        # Three pieces of wood, two specific kinds
        Recipe(["default:wood", "default:wood", "default:pine_wood"],
               "shapeless")

        # Two pieces of wood, each may be one of two kinds
        Recipe([{"default:wood", "default:pine_wood"},
                {"default:wood", "default:pine_wood"}],
               "shapeless")

        # A shaped recipe for a bowl of cat food
        Recipe([[None, ["test:cat_food"], None],
                [None, {"test:cat_bowl", "test:dog_bowl"}, None]])

    def test_ingredients(self):
        """Recipes can return a dict describing their ingredients"""
        r = Recipe(self.woods, "fuel")
        self.assertEqual(
            r.ingredients(),
            {"craft_items": [],
             "groups": [self.woods]})

        r = Recipe(["default:wood", self.metals, self.woods, "default:wood"],
                   "unshaped")
        self.assertEqual(
            r.ingredients(),
            {"craft_items": ["default:wood", "default:wood"],
             "groups": [self.metals, self.woods]})

        r = Recipe([[self.metals], [None, "default:pine_wood"], [self.metals]])
        self.assertEqual(
            r.ingredients(),
            {"craft_items": ["default:pine_wood"],
             "groups": [self.metals, self.metals]})

    def test_sortable(self):
        """Recipes should know whether they can be sorted"""

        # Shaped recipes are never sortable
        r = Recipe([[self.metals], [None, "default:pine_wood"], [self.metals]])
        self.assertFalse(r.sortable())
        r = Recipe([["test:spoon"], ["test:cereal"], ["test:bowl"]])
        self.assertFalse(r.sortable())

        # unshaped recipes are sortable if their ingredients have no Groups
        r = Recipe(["default:wood", self.metals, self.woods, "default:wood"],
                   "unshaped")
        self.assertFalse(r.sortable())
        r = Recipe(["test:spoon", "test:cereal", "test:bowl"], "unshaped")
        self.assertTrue(r.sortable())

    def test_single_item_recipe_conflics(self):
        """Recipes consisting of a single, unshaped Items can detect
        conflicts
        """
        woodItem = Recipe("default:junglewood", "cooking")
        woodGroup = Recipe(self.woods, "cooking")

        self.assertTrue(woodItem.conflicts(woodItem))
        self.assertTrue(woodItem.conflicts(woodGroup))

        self.assertTrue(woodGroup.conflicts(woodGroup))
        self.assertTrue(woodGroup.conflicts(woodItem))

        metalItem = Recipe("default:gold_ingot", "cooking")
        metalGroup = Recipe(self.metals, "cooking")

        self.assertFalse(woodItem.conflicts(metalItem))
        self.assertFalse(woodItem.conflicts(metalGroup))

        self.assertFalse(woodGroup.conflicts(metalGroup))
        self.assertFalse(woodGroup.conflicts(metalItem))

    def test_multi_item_recipe_conflicts(self):
        """Recipes with multiple unshaped Items can detect conflicts"""

        r1 = Recipe([self.woods, self.metals, "test:bowl"], "unshaped")
        r2 = Recipe([self.metals, "test:bowl", self.woods], "unshaped")

        self.assertTrue(r1.conflicts(r1))
        self.assertTrue(r1.conflicts(r2))
        self.assertTrue(r2.conflicts(r1))

        r3 = Recipe(["test:bowl", self.metals], "unshaped")
        self.assertFalse(r3.conflicts(r1))
        self.assertFalse(r1.conflicts(r3))

    def test_identically_shaped_conflicts(self):
        """Shaped recipes with identical shapes can detect conflicts"""

        default_wood_chest = Recipe(
            [["default:wood", "default:wood", "default:wood"],
             ["default:wood", None, "default:wood"],
             ["default:wood", "default:wood", "default:wood"]])
        pine_wood_chest = Recipe(
            [["default:pine_wood", "default:pine_wood", "default:pine_wood"],
             ["default:pine_wood", None, "default:pine_wood"],
             ["default:pine_wood", "default:pine_wood", "default:pine_wood"]])
        woods_chest = Recipe(
            [[self.woods, self.woods, self.woods],
             [self.woods, None, self.woods],
             [self.woods, self.woods, self.woods]])

        self.assertTrue(default_wood_chest.conflicts(default_wood_chest))
        self.assertFalse(default_wood_chest.conflicts(pine_wood_chest))
        self.assertTrue(default_wood_chest.conflicts(woods_chest))

    def test_floating_slab_shape_conflicts(self):
        """Slab shaped recipes with inexact locations can detect conflicts"""

        woods_slab = Recipe([[self.woods, self.woods, self.woods]])

        floating_pine = Recipe([["default:pine_wood",
                                 "default:pine_wood",
                                 "default:pine_wood"],
                                [None, None, None],
                                [None, None, None]])
        sinking_pine = Recipe([[None, None, None],
                               [None, None, None],
                               ["default:pine_wood",
                                "default:pine_wood",
                                "default:pine_wood"]])

        self.assertTrue(woods_slab.conflicts(floating_pine))
        self.assertTrue(woods_slab.conflicts(sinking_pine))
        self.assertFalse(sinking_pine.conflicts(floating_pine))

    def test_floating_cube_shape_conflicts(self):
        """Cubes with inexact locations can detect conflicts"""

        metal_box = Recipe([[self.metals, self.metals],
                            [self.metals, self.metals]])

        metal_corner1 = Recipe([[None, self.metals, self.metals],
                                [None, self.metals, self.metals],
                                [None, None, None]])

        metal_corner2 = Recipe([[None, None, None],
                                [self.metals, self.metals, None],
                                [self.metals, self.metals, None]])

        not_even = Recipe([[self.metals, self.metals],
                           [self.metals]])

        even = Recipe([[self.metals, self.metals],
                       [self.metals, None]])

        unmatched_even = Recipe([[self.metals, self.metals],
                                 [None, self.metals]])

        self.assertTrue(metal_box.conflicts(metal_box))
        self.assertTrue(metal_box.conflicts(metal_corner1))
        self.assertTrue(metal_box.conflicts(metal_corner2))
        self.assertFalse(metal_box.conflicts(not_even))
        self.assertFalse(metal_corner1.conflicts(metal_corner2))
        self.assertFalse(metal_corner1.conflicts(not_even))

        self.assertTrue(not_even.conflicts(not_even))
        self.assertTrue(not_even.conflicts(even))
        self.assertFalse(not_even.conflicts(unmatched_even))

    def test_altered_shapes_dont_conflict(self):
        """Same ingredients, different shape don't conflict"""
        left = Recipe([["default:wood", "default:iron_ingot"]])
        right = Recipe([["default:iron_ingot", "default:wood"]])
        up = Recipe([["default:iron_ingot"], ["default:wood"]])
        down = Recipe([["default:wood"], ["default:iron_ingot"]])

        self.assertTrue(left.conflicts(left))
        self.assertFalse(left.conflicts(right))
        self.assertFalse(left.conflicts(up))
        self.assertFalse(left.conflicts(down))

        self.assertTrue(up.conflicts(up))
        self.assertFalse(up.conflicts(down))
        self.assertFalse(up.conflicts(left))
        self.assertFalse(up.conflicts(right))

    def test_vertical_shapes(self):
        """Matches on vertical shapes should work"""
        vertical = Recipe([["test:thing"], ["test:thing"], ["test:thing"]])

        leftical = Recipe([[None, "test:thing"],
                           [None, "test:thing"],
                           [None, "test:thing"]])
        rightical = Recipe([["test:thing", None],
                            ["test:thing", None],
                            ["test:thing", None]])

        further = Recipe([["test:thing", None, None],
                          ["test:thing", None, None],
                          ["test:thing", None, None]])

        self.assertTrue(vertical.conflicts(vertical))
        self.assertTrue(vertical.conflicts(leftical))
        self.assertTrue(vertical.conflicts(rightical))
        self.assertTrue(vertical.conflicts(further))

        self.assertFalse(leftical.conflicts(rightical))
        self.assertFalse(leftical.conflicts(further))
        self.assertTrue(rightical.conflicts(further))

    def test_normalize_shapes(self):
        """Fill out shaped Recipes of different sizes to compare, if needed"""

        metal_box = Recipe([[self.metals, self.metals],
                            [self.metals, self.metals]])

        metal_corner1 = Recipe([[None, self.metals, self.metals],
                                [None, self.metals, self.metals],
                                [None, None, None]])

        metal_corner2 = Recipe([[None, None, None],
                                [self.metals, self.metals, None],
                                [self.metals, self.metals, None]])

        a, b = Recipe._normalize(metal_box.items, metal_corner1.items)
        self.assertEqual(a, b)
        self.assertEqual(metal_corner1.items, a)

        a, b = Recipe._normalize(metal_corner2.items, metal_box.items)
        self.assertEqual(a, b)
        self.assertEqual(metal_corner2.items, a)

        a, b = Recipe._normalize(metal_corner1.items, metal_corner2.items)
        self.assertNotEqual(a, b)
        self.assertEqual(a, metal_corner1.items)
        self.assertEqual(b, metal_corner2.items)

if __name__ == "__main__":
    unittest.main()
