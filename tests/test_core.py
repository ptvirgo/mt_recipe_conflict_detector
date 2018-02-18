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
        self.assertEqual(r.ingredients(), [self.woods])

        r = Recipe(["default:wood", self.metals, self.woods, "default:wood"],
                   "unshaped")
        self.assertEqual(
            r.ingredients(),
            ["default:wood", self.metals, self.woods, "default:wood"])

        r = Recipe([[self.metals], [None, "default:pine_wood"], [self.metals]])
        self.assertEqual(
            r.ingredients(),
            [self.metals, "default:pine_wood", self.metals])

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

if __name__ == "__main__":
    unittest.main()
