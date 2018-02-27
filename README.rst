Minetest Craft Recipe Conflict Detector
----------------------------------------


[Minetest](https://www.minetest.net/) mods sometimes define the same craft
recipe for different items.  If conflicting recipes are installed on the same
server, some game items will be impossible to craft.  Minetest administrators
can use the detector to identify conflicts, making it easy to reconcile them
before players are affected.

This is a command line tool intended for server administrators.  In order to use
it, as well as to do anything with the information in provides, you'll need to
be:

1. Comfortable understanding and running commands in the
terminal.
2. Prepared to edit plain-text and Minetest recipe code files as needed.

Setup
-----


Linux (should be similar for Mac)
=================================

Linux, command line:

.. code:: bash
     
    $ pip install --user vex  
        # vex is like virtualenv, but with Unix elegance:
        # https://pypi.python.org/pypi/vex
    $ vex --python python3 -m minetest_recipe
    $ git clone git+git://github.com/ptvirgo/mt_recipe_conflict_detector
    $ cd mt_recipe_conflict_checker
    $ pip install ./
    $ cp -r recipe_export ~/.minetest/mods


Windows
=======

I haven't used Windows in over 15 years; if someone wants to sort these out I'm
willing to add instructions here.


Running
-------

- Activate the **recipe_export** mod along with any mods you wish to detect
conflicts for to a Minetest world: named *MyWorld* for this example.
- Start up the Minetest game with your demo world to load the recipes.
- Shut down the game to export them.
- Run 

.. code:: bash
    vex minetest_recipe scripts/detect_conflicts.py ~/.minetest/worlds/MyWorld/recipe_export.json


Results
=======

If you're very, very lucky, there will be no output at all.  Congrats!  No
conflicts.

More likely, you'll see a list of conflicts similar to this sample:

::
    katanas:katana_wood conflicts with katanas:umad_bro
    default:furnace conflicts with xdecor:stone_rune
    "gates_wooden:classic" conflicts with doors:gate_wood_closed
    itemframes:frame conflicts with frame:empty
    ...

In the example above, an admin would likely want to remove or alter the recipe
for the fictional "katanas:umad_bro" item, as well as the rest of them.

If a line appears stating that a recipe conflicts with itself, that means the
same recipe is being loaded by your server twice.
