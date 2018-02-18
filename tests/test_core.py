#/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from recipe import Craft, Recipe


class TestRecipe(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
