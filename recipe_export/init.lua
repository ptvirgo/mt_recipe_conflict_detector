--[[

Recipe exporter for Minetest

]]--

local output_file = minetest.get_worldpath().."/exported_recipes.json"

local i = 0
local recipes = {}

local mtrc = minetest.register_craft
minetest.register_craft = function(options)
    mtrc(options)
    recipes[i] = options
    i = i + 1
end

minetest.register_on_shutdown(function()

    local f = assert(io.open(output_file, "w"))
    f:write("[\n")

    local j
    for j=0, (i - 1) do
        local json_string = minetest.write_json(recipes[j])
        f:write(json_string)

        if j < (i - 1) then
            f:write(",\n")
        end
    end

    f:write("]")
    f:close()
end)
