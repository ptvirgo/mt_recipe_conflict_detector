#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from recipe import CraftItem


class TestCraftItems(unittest.TestCase):
    """CraftItem creation"""

    def test_naming(self):
        """CraftItem names"""
        wood = CraftItem("default:wood")
        wood2 = CraftItem(":default:wood")

        self.assertEqual(wood.name, "default:wood")
        self.assertEqual(wood2.name, "default:wood")


    def test_craft_item_equality(self):
        """CraftItems with the same name are equal"""

        steel = CraftItem("default:steel_ingot")
        steel2 = CraftItem("default:steel_ingot")
        gold = CraftItem("default:gold_ingot")

        self.assertEqual(steel, steel2)
        self.assertNotEqual(steel, gold)
