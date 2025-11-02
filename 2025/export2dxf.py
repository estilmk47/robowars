import bpy
import bmesh

import sys
import os

root = bpy.data.filepath        # The filepath of the .blend file you run the script in
root = os.path.dirname(root)    # The repo you are working in [most likely]
sys.path.append(root+'\\venv\Lib\site-packages')
import ezdxf


def save_object_as_dxf(object, path, scale = 1.0):
    bm = bmesh.new()
    bm.from_mesh(object.data)
    bm.edges.ensure_lookup_table()

    # Create a new DXF document
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Convert edges to DXF lines
    for edge in bm.edges:
        verts = edge.verts
        start = verts[0].co  # Start vertex of the edge
        end = verts[1].co    # End vertex of the edge
        msp.add_line(start=(start.x*scale, start.y*scale), end=(end.x*scale, end.y*scale))

    # Save the DXF file
    doc.saveas(path)
    print(f"Edges of object '{object.name}' successfully exported to '{path}'.")
    bm.free()
    
    
if __name__ == '__main__':
    name = "chassi_floor"
    
    filename = "output/"+name+".dxf" 
    path = os.path.join(root, filename)
    
    object = bpy.data.objects.get(name)
    if object is None:
        print(f"Object with name '{name}' not found.")
    else:
        if object.type != 'MESH':
            print(f"Object '{name}' is not a mesh.")
        else:
            save_object_as_dxf(object, path)