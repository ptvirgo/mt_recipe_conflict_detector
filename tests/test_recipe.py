#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from recipe import Craft, Recipe


class TestCraft(unittest.TestCase):
    """Check Craft object"""

    def test_shaped_from_dict(self):
        """Craft items can be constructed from dicts, shaped by default"""
        axe_dict = {
            "output":"default:axe_steel",
            "recipe":[["default:steel_ingot","default:steel_ingot"],
                      ["default:steel_ingot","group:stick"],
                      ["","group:stick"]]}


        axe = Craft.from_dict(axe_dict)
        self.assertEqual(axe.output, axe_dict["output"])

        self.assertEqual(axe.recipe.craft_type, "shaped")
        for i in range(len(axe_dict["recipe"])):
            self.assertEqual(axe.recipe.craft_items[i], axe_dict["recipe"][i])


    def test_shapeless_from_dict(self):
        """Craft items constructed from dicts get the correct craft_type"""
        chest_dict = {
            "output":"default:chest_locked",
            "recipe":["default:chest","default:steel_ingot"],
            "type":"shapeless"}


        chest = Craft.from_dict(chest_dict)

        self.assertEqual(chest.output, chest_dict["output"])
        self.assertEqual(chest.recipe.craft_type, chest_dict["type"])

        for i in range(len(chest_dict["recipe"])):
            self.assertEqual(chest.recipe.craft_items[i], chest_dict["recipe"][i])
