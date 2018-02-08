--[[

Recipe exporter for Minetest

]]--

local output_file = minetest.get_worldpath().."/exported_groups.json"

local groups = {}

local mtrn = minetest.register_node

minetest.register_node = function(name, options)
    mtrn(name, options)

    for gid, cnt in pairs(options["groups"]) do

        if groups[gid] == nil then
            groups[gid] = {}
        end

        if (cnt ~= nil and cnt > 0) then
            table.insert(groups[gid], name)
        end 
    end
end

minetest.register_on_shutdown(function()

    local f = assert(io.open(output_file, "w"))
    local json_string = minetest.write_json(groups)
    f:write(json_string)
    f:close()
end)
