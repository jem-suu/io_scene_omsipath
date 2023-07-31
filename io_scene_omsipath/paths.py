import re
from bpy import path, data
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
        mesh = data.meshes.new(obj_name)
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

        obj = data.objects.new(obj_name, mesh)

        scn = context.scene
        scn.collection.objects.link(obj)
        obj.select_set(state = True)

        return ""
    else:
        return "\nError: The chosen file does not contain any pathpoints\n-> Solution: Choose a correct path file."
