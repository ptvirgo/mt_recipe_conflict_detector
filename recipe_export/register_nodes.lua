--[[
    Copyright 2018 Pablo Virgo.

    This file is part of mt_recipe_conflict_detector.

    mt_recipe_conflict_detector is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    mt_recipe_conflict_detector is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with mt_recipe_conflict_detector.  If not, see <http://www.gnu.org/licenses/>.

]]

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
