import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy_extras.object_utils import AddObjectHelper

from . import paths, passengercabin

bl_info = {
    "name": "OMSI Pax Configuration File Exporter",
    "description": "Import-Export passenger configuration files for OMSI.",
    "author": "Fabian S., jem_suu",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import/Export > OMSI Passenger/Path Config (.cfg)",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/jem-suu/io_scene_omsipath",
    "tracker_url": "https://github.com/jem-suu/io_scene_omsipath/issues",
    "support": "TESTING",
    "category": "Import-Export",
}

# Path Import

class ImportPaths(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.paths"
    bl_label = "Import Path Config"

    filepath = StringProperty(subtype='FILE_PATH')
    
    def execute(self, context):
        paths.path_import(self.filepath, context)
        return {'FINISHED'}

def menu_func_importpaths(self, context):
    self.layout.operator(ImportPaths.bl_idname, text="OMSI Path Config (.cfg)")

# Path Export

# PassengerCabin Export

# Register/Unregister plugin

def register():
    bpy.utils.register_class(ImportPaths)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importpaths)

def unregister():
    bpy.utils.unregister_class(ImportPaths)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importpaths)

if __name__ == "__main__":
    register()