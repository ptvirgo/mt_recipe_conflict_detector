#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from recipe import helpers
from recipe.item import CraftItem, Group


class TestHelpers(unittest.TestCase):
    """Recipe checker helper function unit tests"""

    def test_craft_or_group_makes_groups(self):
        """String describing a group should return a Group"""

        group = helpers.item_or_group("group:wood")
        self.assertIsInstance(group, Group)
        self.assertEqual(group.name, "wood")

    def test_craft_or_group_makes_crafts(self):
        """String describing a craft item should return a CraftItem"""

        craft_item = helpers.item_or_group("default:diamond")
        self.assertIsInstance(craft_item, CraftItem)
        self.assertEqual(craft_item.name, "default:diamond")


    def test_names_to_items(self):
        """names_to_items can produce recipe item collections"""

        self.assertEqual(helpers.names_to_items("default:wood"),
                         [[CraftItem("default:wood")]])

        self.assertEqual(helpers.names_to_items(
            ["default:steel_ingot",
             "default:bronze_ingot",
             "default:gold_ingot"]),
            [[CraftItem("default:steel_ingot"),
              CraftItem("default:bronze_ingot"),
              CraftItem("default:gold_ingot")]])



if __name__ == "__main__":
    unittest.main()
