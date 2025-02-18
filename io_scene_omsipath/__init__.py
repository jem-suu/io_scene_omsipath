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

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper

from . import paths, passengercabin

bl_info = {
    "name": "OMSI Pax Configuration File Exporter",
    "description": "Import-Export passenger configuration files for OMSI.",
    "author": "Fabian S., jem_suu",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import/Export > OMSI Passenger/Path Config (.cfg)",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/jem-suu/io_scene_omsipath",
    "tracker_url": "https://github.com/jem-suu/io_scene_omsipath/issues",
    "category": "Import-Export",
}

# Path Import

class ImportPaths(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.paths"
    bl_label = "Import Path Config"

    # filepath = StringProperty(subtype='FILE_PATH')
    
    def execute(self, context):
        paths.path_import(self.filepath, context)
        return {'FINISHED'}

def menu_func_importPaths(self, context):
    self.layout.operator(ImportPaths.bl_idname, text="OMSI Path Config (.cfg)")

# Path Export

class ExportPaths(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.paths"
    bl_label = "Export OMSI Path config"

    filename_ext = ".cfg"

    # filepath = StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        errors = ""
        errors += paths.path_export(self.filepath, context)

        if len(errors):
            raise Exception(errors)
        return {'FINISHED'}

def menu_func_exportPaths(self, context):
    self.layout.operator(ExportPaths.bl_idname, text="OMSI Path Config (.cfg)")

# PassengerCabin Export

# Register/Unregister plugin

def register():
    bpy.utils.register_class(ImportPaths)
    bpy.utils.register_class(ExportPaths)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importPaths)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_exportPaths)

def unregister():
    bpy.utils.unregister_class(ImportPaths)
    bpy.utils.unregister_class(ExportPaths)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importPaths)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_exportPaths)

if __name__ == "__main__":
    register()