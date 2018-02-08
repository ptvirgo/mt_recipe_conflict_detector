--[[

Recipe exporter for Minetest

]]--

node_export.data["recipes"] = {}
local mtrc = minetest.register_craft

minetest.register_craft = function(options)
    mtrc(options)
    table.insert(node_export.data["recipes"], options)
end
