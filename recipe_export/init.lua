node_export = {}
node_export.data = {}

local mod_path = minetest.get_modpath("recipe_export")
local output_file = minetest.get_worldpath().."/recipe_export.json"

dofile(mod_path.."/register_crafts.lua")
dofile(mod_path.."/register_nodes.lua")

minetest.register_on_shutdown(function()

    local f = assert(io.open(output_file, "w"))
    local json_string = minetest.write_json(node_export.data)
    f:write(json_string)
    f:close()
end)
