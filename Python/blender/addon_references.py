import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

bl_info = {
    "name": "Modeler",
    "description": "Export 3D meshes with references",
    "author": "Loïc NORGEOT",
    "version": (0, 0),
    "blender": (2, 76, 0),
    "warning": "",
    "category": "Import-Export"}

class Settings(PropertyGroup):
    triangulate = BoolProperty(name="triangulate",
                               description="Triangulate the mesh",
                               default = False)
    file = StringProperty(name = "file",
                          default = "./out.mesh",
                          description = "File to be exported to",
                          subtype = 'FILE_PATH')

class Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Tools"
    bl_label = "Export refernces"
    
    def draw(self, context):
        mytool = context.scene.my_tool
        self.layout.prop(mytool, "file", text="Output mesh")
        self.layout.prop(mytool, "triangulate", text="Triangulate")
        TheCol = self.layout.column(align=True)
        TheCol.operator("modeler.refs", text="Export mesh")

class run(bpy.types.Operator):
    bl_idname = "modeler.refs"
    bl_label = "Export and remesh"

    def invoke(self, context, event):
        T = context.scene.my_tool
        scene = bpy.context.scene

        nbMeshes = len([o for o in scene.objects if o.type=="MESH"])
        if nbMeshes>1:
            for obj in scene.objects:
                if obj.type == "MESH":
                    obj.select = True
                else:
                    obj.select = False
            bpy.ops.object.join()

        obj = bpy.context.scene.objects.active
                
        if T.triangulate:
            obj.modifiers.new("triangulate", "TRIANGULATE")

        mesh = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
        verts = mesh.vertices
        triangles = [f for f in mesh.tessfaces]

        refs = [poly.material_index for poly in mesh.polygons]

        fp = open(T.file, 'w')
        fp.write('MeshVersionFormatted 1\nDimension 3\n')
        fp.write("Vertices\n")
        fp.write(str(len(verts)))
        fp.write("\n")

        for v in verts:
            x = v.co[0]
            y = v.co[1]
            z = v.co[2]
            fp.write(str(x) + " " + str(y) + " " + str(z) + " " + str(0) + "\n")
        if T.triangulate:
            fp.write("Triangles\n")
        else:
            fp.write("Quadrilaterals\n")
        fp.write(str(len(triangles))) 
        fp.write("\n")

        for t,r in zip(triangles, refs):
            for v in t.vertices:
                fp.write(str(v+1))
                fp.write(" ")
            fp.write(str(r))
            fp.write('\n')
        fp.close()

        bpy.data.meshes.remove(mesh)

        return {"FINISHED"}

bpy.utils.register_class(run)
bpy.utils.register_class(Panel)

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=Settings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
