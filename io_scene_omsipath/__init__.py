import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy_extras.object_utils import AddObjectHelper

import paths

bl_info = {
    "name": "OMSI Passenger Cabin / Paths Importer & Exporter",
    "description": "Imports Path config files and Exports Passenger Positions and Paths to config files",
    "author": "Fabian S., jem_suu",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import/Export > OMSI PassengerCabin/Path config",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "",
    "tracker_url": "",
    "support": "TESTING",
    "category": "Import-Export",
}

class ImportPaths(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.paths"
    bl_label = "Import OMSI Path config"
    
    def execute(self, context):
        paths.path_import(self.filepath, context)
        return {'FINISHED'}

    
def menu_func_importpaths(self, context):
    self.layout.operator(ImportPaths.bl_idname, text="OMSI Path Config (.cfg)")

def register():
    bpy.utils.register_class(ImportPaths)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importpaths)

def unregister():
    bpy.utils.unregister_class(ImportPaths)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importpaths)

if __name__ == "__main__":
    register()