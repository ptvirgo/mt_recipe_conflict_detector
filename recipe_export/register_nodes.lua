--[[

Recipe exporter for Minetest

]]--

node_export.data["groups"] = {}

local mtrn = minetest.register_node
minetest.register_node = function(name, options)
    mtrn(name, options)

    for gid, cnt in pairs(options["groups"]) do

        if node_export.data["groups"][gid] == nil then
            node_export.data["groups"][gid] = {}
        end

        if (cnt ~= nil and cnt > 0) then
            table.insert(node_export.data["groups"][gid], name)
        end 
    end
end
