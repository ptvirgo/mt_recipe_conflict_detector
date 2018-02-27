Developer notes
---------------


Lingo / Data definitions
========================

For the purposes of the code, I adopted the following lingo.  Based as best as I
could on existing, documented terms.

CraftItem
    A string representation of a single, specific item as can be used in the Minetest inventory or craft table.

    - None or an empty string can represent a CraftItem
    - Validators should convert empty strings to None
    - CraftItems may appear with a leading ":", which should be removed for our purposes.
    - *Examples:* "default:steel_ingot" or "default:diamond"

GroupName
    A string representation of a named collection of Minetest Craftitems.

    - The string must lead with the characters "group:"
    - *Examples:* "group:stick" or "group:wood"

Group
    A python set containing CraftItems

    - Groups should not contain the empty string or None
    - Groups should reflect the set of Items expected per their related GroupName
    - *Example:* {"default:steel_ingot, "default:diamond"}

Item
    Craft be a CraftItem, Group, or None.

RecipeCollection
    May be:

    - an Item
    - a list of up to 9 Items
    - a list containing up to 3 lists of up to 3 items, ie:
      [[Item, Item, Item], [Item, Item, Item], [Item, Item, Item]]

CraftType
    A string representing the "kind" of a given Recipe, per the Minetest game.

    - "shaped", "shapeless", "fuel", and "cooking" are standard.
    - "shaped" is the default.
    - Other CraftType strings may be introduced by Minetest mods.
