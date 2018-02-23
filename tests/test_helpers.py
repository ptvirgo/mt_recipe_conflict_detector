#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mt_crafting_recipe import helpers


class TestHelpers(unittest.TestCase):
    """Test the helper functions"""

    def test_item_name(self):
        """Item names should have initial colons stripped"""
        self.assertEqual(helpers.item_name("default:steel_ingot"),
                         "default:steel_ingot")

        self.assertEqual(helpers.item_name(":default:steel_ingot"),
                         "default:steel_ingot")

        self.assertEqual(helpers.item_name("default:coal 9"),
                         "default:coal")

    def test_collection_map(self):
        """Mapping over the typical RecipeCollection structure works as
        expected.
        """
        self.assertEqual(helpers.map_recipe_collection(int, "1"), 1)
        self.assertEqual(helpers.map_recipe_collection(int, ["1", "2", "3"]),
                         [1, 2, 3])
        self.assertEqual(
            helpers.map_recipe_collection(int, [["1", "2"], ["3"]]),
            [[1, 2], [3]])

    def test_collection_reduce(self):
        """Reducing typical RecipeCollection works as expected."""

        def merge(a, b):
            return a + b

        self.assertEqual(helpers.reduce_recipe_collection(
            merge, "default:wood", "x"),
            "xdefault:wood")

        self.assertEqual(helpers.reduce_recipe_collection(
            merge, ["default:wood", "test:bowl"], "x"),
            "xdefault:woodtest:bowl")

        self.assertEqual(helpers.reduce_recipe_collection(
            merge, [["1", "2"], ["3", "4"], ["5", "6", "7"]], "x"),
            "x1234567")

    def test_items_match(self):
        """We should detect potential item conflicts"""
        woods = {"default:pine_wood", "default:jungle_wood", "default:wood"}
        metals = {"default:steel_ingot", "default:bronze_ingot",
                  "default:gold_ingot"}
        everything = woods.union(metals)

        self.assertTrue(helpers.items_match("default:steel_ingot",
                                            "default:steel_ingot"))
        self.assertFalse(helpers.items_match("default:steel_ingot",
                                             "default:bronze_ingot"))

        self.assertTrue(helpers.items_match("default:steel_ingot", metals))
        self.assertTrue(helpers.items_match(metals, "default:steel_ingot"))

        self.assertFalse(helpers.items_match("default:steel_ingot", woods))
        self.assertFalse(helpers.items_match(woods, "default:steel_ingot"))

        self.assertTrue(helpers.items_match(woods, woods))
        self.assertFalse(helpers.items_match(metals, woods))
        self.assertFalse(helpers.items_match(everything, metals))

if __name__ == "__main__":
    unittest.main()
