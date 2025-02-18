# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import re
import bpy
from time import strftime

def path_import(filepath, context):
    obj_name = bpy.path.display_name(filepath)

    # Read path data:
    with open(filepath, "r") as file:
        path_data = file.read()
        
        # Read pathpoints:
        pathpnts = re.findall(r"\[pathpnt\]\n(-?\d+(?:\.\d+)?)\n(-?\d+(?:\.\d+)?)\n(-?\d+(?:\.\d+)?)", path_data)
        
        # Read pathlinks:
        pathlinks = re.findall(r"(?:\[pathlink\]|\[pathlink_oneway\])\n(\d+)\n(\d+)", path_data)
        #oneway = re.findall(r"\[pathlink_oneway\]\n(\d+)\n(\d+)", path_data)

        # Convert them to the right format:
        pathpnts = [tuple(map(float, pnt)) for pnt in pathpnts]
        pathlinks = [list(map(int, lnk)) for lnk in pathlinks]
        #oneway = [tuple(map(int, ow)) for ow in oneway]

        """
        # Roomheights:
        roomheights = []
        height_in_next_line = False
        file.seek(0)
        for line in file:
            if line == "[next_roomheight]\n":
                height_in_next_line = True
            elif height_in_next_line:
                height_in_next_line = False
                roomheights.append(float(line[:-1])/10)
            elif line == "[pathlink]\n" or line == "[pathlink_oneway]\n":
                roomheights.append(roomheights[-1])
        """

    # Create mesh with given data:
    if len(pathpnts):
        mesh = bpy.data.meshes.new(obj_name)
        mesh.from_pydata(pathpnts, pathlinks, [])
    
        """
        # Add crease and bevel weight:
        for i in range(len(mesh.edges)):
            ids = (mesh.edges[i].vertices[0], mesh.edges[i].vertices[1])
            if ids in oneway:
                mesh.edges[i].crease = 1

            mesh.edges[i].bevel_weight = roomheights.pop(0)

        mesh.update()
        """

        obj = bpy.data.objects.new(obj_name, mesh)

        scn = context.scene
        scn.collection.objects.link(obj)
        obj.select_set(state = True)

        return ""
    else:
        return "\nError: The chosen file does not contain any pathpoints\n-> Solution: Choose a correct path file."

def path_export(filepath, context):
    errors = ""

    # Get path object (=selected object):
    try:
        path = context.selected_objects[0]
    except IndexError:
        try:
            path = context.scene.objects["Paths"]
        except KeyError:
            return "\nError: No object with name \"Paths\" was found\n-> Solution: Rename the paths object."

    with open(filepath, "w") as file:
        # Timestamp in first line:
        file.write("This file was created with OMSI Configuration File Exporter for Blender (%s)\n" % strftime("%Y-%m-%d %H:%M:%S"))

        # Pathpoints:
        file.write("\n---------------------------\nPathpoints:\n")
        if len(path.data.vertices):
            for v in path.data.vertices:
                file.write("\n%d\n[pathpnt]\n%.3f\n%.3f\n%.3f\n" % (v.index, v.co.x, v.co.y, v.co.z))

            # Pathlinks:
            file.write("\n---------------------------\nPathlinks:\n")
            if len(path.data.edges):
                last_height = 0
                for e in sorted(path.data.edges, key=lambda x: x.vertices[0]):
                    if e.bevel_weight != last_height and e.bevel_weight > 0:
                        last_height = e.bevel_weight
                        file.write("\n[next_roomheight]\n%.2f\n" % (last_height*10))
                    if e.crease:
                        file.write("\n[pathlink_oneway]\n%d\n%d\n" % tuple(e.vertices))
                    else:
                        file.write("\n[pathlink]\n%d\n%d\n" % tuple(e.vertices))
            else:
                errors += "\nError: The selected object has no edges\n-> Solution: Add edges."
        else:
            errors += "\nError: The selected object has no vertices\n-> Solution: Add vertices."

        return errors
