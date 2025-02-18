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
from math import atan, degrees
import random

def export(filepath, context):
    errors = "\nWarning: No driver seat defined!\n-> Solution: A driver seat can be defined by setting the crease value of an edge."

    # Get path object (=selected object or object named "Passengercabin"):
    try:
        passengercabin = context.scene.objects["PassengerCabin"]
    except KeyError:
        try:
            passengercabin = context.selected_objects[0]
        except IndexError:
            return "\nError: No object with name \"PassengerCabin\" was found\n-> Solution: Rename the passengercabin object."

    # Get object data
    edges = passengercabin.data.edges
    verts = passengercabin.data.vertices

    with open(filepath, "w") as file:
        # Timestamp in first line:
        file.write("This file was created with OMSI Configuration File Exporter for Blender (%s)\n" % strftime("%Y-%m-%d %H:%M:%S"))
        
        # Driver seat:
        for e in edges:
            if e.crease != 0:
                errors = ""
                vs = sorted([passengercabin.matrix_world @ verts[e.vertices[0]].co, passengercabin.matrix_world @ verts[e.vertices[1]].co], key=lambda v: v[2])
                try:
                    rot = degrees(atan((vs[0][0]-vs[1][0])/(vs[0][1]-vs[1][1])))
                except ZeroDivisionError:
                    if vs[0][0]-vs[1][0] > 0:
                        rot = 90
                    elif vs[0][0]-vs[1][0] < 0:
                        rot = -90
                    else:
                        rot = 0
                else:
                    if -0.1 < rot < 0.1 and vs[0][1] < vs[1][1]:
                        rot = 180

                file.write("\n###################################\n\nFahrersitz:\n\n[drivpos]\n%.3f\n%.3f\n%.3f\n%.3f\n%d\n"
                           % (vs[1][0], vs[1][1], vs[1][2], vs[1][2]-vs[0][2], rot))
                break

        # Passenger seats:
        file.write("\n###################################\n\nSitze\n")
        for e in edges:
            if e.crease == 0:
                vs = sorted([passengercabin.matrix_world @ verts[e.vertices[0]].co, passengercabin.matrix_world @ verts[e.vertices[1]].co], key=lambda v: v[2])
                try:
                    rot = degrees(atan((vs[0][0]-vs[1][0])/(vs[0][1]-vs[1][1])))
                except ZeroDivisionError:
                    if vs[0][0]-vs[1][0] > 0:
                        rot = 90
                    elif vs[0][0]-vs[1][0] < 0:
                        rot = -90
                    else:
                        rot = 0
                else:
                    if vs[0][1] < vs[1][1]:
                        rot += 180

                if e.bevel_weight:
                    height = 0
                    rot = random.uniform(0, 360)
                else:
                    height = vs[1][2]-vs[0][2]

                file.write("\n[passpos]\n%.3f\n%.3f\n%.3f\n%.3f\n%d\n" % (vs[1][0], vs[1][1], vs[1][2], height, rot))


        if not len(edges):
            errors += "\nWarning: No seats defined!\n-> Solution: Add edges to the mesh."

    return errors
