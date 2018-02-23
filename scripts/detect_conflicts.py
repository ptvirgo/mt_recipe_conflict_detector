#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import warnings

from recipe import Recipe, Craft, helpers


def detect_conflicts(filename):
    """Detect recipe conflicts in a given recipe_export.json"""
    with open(filename, "r") as f:
        data = json.loads(f.read())
    
    groups = get_groups(data["groups"])
    recipe_collection = get_recipes(groups, data["recipes"])
    
    for c in recipe_collection.keys():
        sortables = recipe_collection[c]["sortable"]
        sortable_len = len(sortables)
        unsortables = recipe_collection[c]["unsortable"]
        unsortable_len = len(unsortables)

        i = 0

        while i < sortable_len:
            j = i + 1

            while j < sortable_len:

                if sortables[i].recipe.conflicts(sortables[j].recipe):
                    yield "{} conflicts with {}".format(
                        sortables[i].output, sortables[j].output)
                else:
                    break
                j += 1

            for unsortable in unsortables:
                if sortables[i].recipe.conflicts(unsortable.recipe):
                    yield "{} conflicts with {}".format(
                        sortables[i].output, unsortable)
            i += 1
            
        for i in range(unsortable_len):
            j = i + 1

            while j < unsortable_len:
                if unsortables[i].recipe.conflicts(unsortables[j].recipe):
                    yield "{} conflicts with {}".format(
                        unsortables[i].output, unsortables[j].output)
                j += 1

def get_groups(group_data):
    """From the group data, produce a dict of
    {GroupName: {Craft, Craft}, ...}
    """
    groups = {}

    for g, craft_items in group_data.items():
        group_name = helpers.group_name(g)

        if craft_items is None:
            warnings.warn("Empty group {group_name}".format(
                group_name=group_name))
            continue

        items = set()

        for item in craft_items:
            items.add(helpers.item_name(item))

        if group_name in groups:
            groups[group_name] = groups[group_name].union(items)
        else:
            groups[group_name] = items

    return groups

def get_recipes(groups, recipe_data):
    """From the recipe data, produce a dict of
    {Craft Type { sortable: [Craft ..],
                  unsortable: [Craft ..]}
    """
    recipes = {}
    for r in recipe_data:
        craft = data_to_craft(groups, r)

        if craft is None:
            continue

        if craft.recipe.craft_type in ["shaped", "shapeless"]:
            craft_type = "craft_grid"
        else:
            craft_type = craft.recipe.craft_type

        if not craft_type in recipes:
            recipes[craft_type] = \
                {"sortable": [], "unsortable": []}

        if craft.recipe.sortable():
            recipes[craft_type]["sortable"].append(craft)
        else:
            recipes[craft_type]["unsortable"].append(craft)

    for craft_type in recipes.keys():
        recipes[craft_type]["sortable"] = sorted(
            recipes[craft_type]["sortable"],
            key = lambda craft: craft.recipe.ingredients()["craft_items"])

    return recipes

def data_to_craft(groups, data):
    """Convert the data about a specific recipe into a Craft, or None
    """
    def item_or_group(text):
        if text is None or text == "":
            return

        if text[:6] == "group:":
            group_name = helpers.group_name(text)

            try:
                group = groups[group_name]
            except KeyError as err:
                return "empty_group:{}".format(group_name)

            return group

        else:
            return helpers.item_name(text)
    # end item_or_group closure

    if not "output" in data:
        return

    if not "recipe" in data:
        return

    collection = helpers.map_recipe_collection(
        item_or_group, data["recipe"])

    if "type" in data:
        recipe = Recipe(collection, data["type"])
    else:
        recipe = Recipe(collection)

    craft = Craft(recipe, helpers.item_name(data["output"]))
    return craft

def main():
    parser = argparse.ArgumentParser(
        description="Detect Minetest Recipe Conflicts")

    parser.add_argument("data", type=str,
        help="recipe_export.json, as created by the recipe_export mod")

    args = parser.parse_args()

    for line in detect_conflicts(args.data):
        print(line)

if __name__ == "__main__":
    main()
