#####
# Addon for Import/Export of .mesh files
# TODO: add a saving option for sol files
#####

import os
import bpy
import mathutils

from bpy.props import (BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    )
from bpy_extras.io_utils import (ImportHelper,
    ExportHelper,
    unpack_list,
    unpack_face_list,
    axis_conversion,
    )

bl_info = {
    "name": "MESH format",
    "description": "Import-Export MESH, Import/export simple .MESH file.",
    "author": "Loïc NORGEOT",
    "version": (0, 0),
    "blender": (2, 76, 0),
    "location": "File > Import-Export",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Import-Export"}

class ImportMESH(bpy.types.Operator, ImportHelper):
    """Load a .mesh file"""
    bl_idname = "import_mesh.mesh"
    bl_label = "Import MESH mesh"
    filename_ext = ".mesh"
    filter_glob = StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )

    axis_forward = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
                   ),
            default='Y',
            )
    axis_up = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Z',
            )

    def execute(self, context):

        keywords = self.as_keywords(ignore=('axis_forward',
            'axis_up',
            'filter_glob',
        ))
        global_matrix = axis_conversion(from_forward=self.axis_forward,
            from_up=self.axis_up,
            ).to_4x4()

        meshes = load(self, context, **keywords)
        if not meshes:
            return {'CANCELLED'}

        scene = context.scene

        for m in meshes:
            obj = bpy.data.objects.new(m.name, m)
            scene.objects.link(obj)
            scene.objects.active = obj
            obj.select = True
            obj.matrix_world = global_matrix

        scene.update()

        return {'FINISHED'}

class ExportMESH(bpy.types.Operator, ExportHelper):
    """Save a Mesh file"""
    bl_idname = "export_mesh.mesh"
    bl_label = "Export Mesh file"
    filter_glob = StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )
    check_extension = True
    filename_ext = ".mesh"

    axis_forward = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
                   ),
            default='Y',
            )
    axis_up = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Z',
            )

    def execute(self, context):
        keywords = self.as_keywords(ignore=('axis_forward',
            'axis_up',
            'filter_glob',
            'check_existing',
        ))
        global_matrix = axis_conversion().to_4x4()
        keywords['global_matrix'] = global_matrix
        return save(self, context, **keywords)

def menu_func_import(self, context):
    self.layout.operator(ImportMESH.bl_idname, text="Mesh format (.mesh)")

def menu_func_export(self, context):
    self.layout.operator(ExportMESH.bl_idname, text="Mesh format (.mesh)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

def load(operator, context, filepath):
    # Parse mesh from MESH file
    filepath = os.fsencode(filepath)
    file = open(filepath, 'r')

    verts = []
    triangles = []
    refs = []
    nV = 0
    nT = 0
    readVertices = False
    readTriangles = False

    iV = iT = 0

    with open(filepath, 'r') as f:

        for line in f:

            #Vertices reading
            if (readVertices and (nV>0)):
                if(iV<nV):
                    try:
                        px, py, pz = [float(x) for x in line.split()[:3]]
                        id = int(line[3])
                    except ValueError:
                        print(line.split()[:3])
                    iV += 1
                    verts.append((px, py, pz))
                else:
                    readVertices = False

            #Triangles reading
            if (readTriangles and (nT>0)):
                if(iT<nT):
                    try:
                        px, py, pz, r = [int(x)-1 for x in line.split()[:4]]
                    except ValueError:
                        print(line.split()[:3])
                    iT += 1
                    triangles.append((px, py, pz,r))
                    refs.append(r)
                else:
                    readTriangles = False
                    
            #Number recording
            if (readVertices and (nV == 0)):
                nV = int(line.split()[0])
            if (readTriangles and (nT == 0)):
                nT = int(line.split()[0])
            
            #Reading activation
            try:
                if (line.split() == ["Vertices"]):
                    readVertices = True
                if (line.split() == ["Triangles"]):
                    readTriangles = True
            except:
                print("Aight")

        print("FILE OPENED")
        print("NUMBER OF VERTICES  = ", nV)
        print("NUMBER OF TRIANGLES = ", nT)

    meshes = []

    triangleArray = []
    REFS = set(refs)
    for i,r in enumerate(REFS):
        refTriangles = [t[:3] for t in triangles if t[3]==r]
        # Assemble mesh
        mesh_name = bpy.path.display_name_from_filepath(filepath)
        mesh = bpy.data.meshes.new(name=mesh_name)
        meshes.append(mesh)
        mesh.from_pydata(verts, [], refTriangles)
        mesh.validate()
        mesh.update()

    return meshes


def save(operator, context, filepath, global_matrix = None):
    # Export the selected mesh
    APPLY_MODIFIERS = True # TODO: Make this configurable
    if global_matrix is None:
        global_matrix = mathutils.Matrix()
    scene = context.scene
    obj = scene.objects.active
    mesh = obj.to_mesh(scene, APPLY_MODIFIERS, 'PREVIEW')

    # Apply the inverse transformation
    obj_mat = obj.matrix_world
    #mesh.transform(global_matrix * obj_mat)

    verts = mesh.vertices[:]
    triangles = [ f for f in mesh.tessfaces ]

    # Write geometry to file
    meshFile = os.fsencode(filepath)
    fp = open(meshFile, 'w')
    fp.write('MeshVersionFormatted 1\nDimension 3\n')
    fp.write("Vertices\n")
    fp.write(str(len(verts)))
    fp.write("\n")
    for v in verts:
        x = v.co[0]
        y = v.co[1]
        z = v.co[2]
        #print(x,y,z)
        fp.write(str(x) + " " + str(y) + " " + str(z) + " " + str(1) + "\n")
    fp.write("Triangles\n")
    fp.write(str(len(triangles))) 
    fp.write("\n")
    for t in triangles:
        for v in t.vertices:
            fp.write(str(v+1))
            fp.write(" ")
        fp.write(str(1))
        fp.write('\n')
    fp.close()

    #Write sol file
    solFile = None

    """
    if(obj.data.vertex_colors):
        hmin = 0.0025 * max(bpy.context.object.dimensions) # 0.25 %
        hmax = 0.02  * max(bpy.context.object.dimensions) # 2 %
        try:
            T = bpy.context.scene.my_tool
            print(T)
            hmin = T.hmin/100.0 * max(bpy.context.object.dimensions)  
            print(hmin)
            hmax = T.hmax/100.0 * max(bpy.context.object.dimensions)
        except:
            print("MMG Addon not installed -> hmin = 0.25 %, hmax = 2%")
        solFile = filepath[:-5] + ".sol"
        fp = open( os.fsencode(solFile), 'w')
        fp.write("MeshVersionFormatted 2\n")
        fp.write("Dimension 3\n")
        fp.write("SolAtVertices\n")
        fp.write(str(len(verts)))
        fp.write("\n1 1\n") 
        #Compute colors
        vertex_color = obj.data.vertex_colors.active.data
        print(len(vertex_color))
        cols = [None] * len(verts)
        for i,t in enumerate(triangles):
            for j,v in enumerate(t.vertices):
                cols[v] = float(vertex_color[3*i + j].color.r)
        for c in cols:
            fp.write('%.8f' % (hmin + c * (hmax-hmin)))
            fp.write("\n")
        fp.close()
    """



    #WEIGHT PAINT
    vgrp=bpy.context.active_object.vertex_groups.keys()
    if(len(vgrp)>0):
        hmin = 0.0025 * max(bpy.context.object.dimensions) # 0.25 %
        hmax = 0.02  * max(bpy.context.object.dimensions) # 2 %
        try:
            T = bpy.context.scene.my_tool
            print(T)
            hmin = T.hmin/100.0 * max(bpy.context.object.dimensions)  
            print(hmin)
            hmax = T.hmax/100.0 * max(bpy.context.object.dimensions)
        except:
            print("MMG Addon not installed -> hmin = 0.25 %, hmax = 2%")
        
        solFile = filepath[:-5] + ".sol"
        fp = open( os.fsencode(solFile), 'w')
        fp.write("MeshVersionFormatted 2\n")
        fp.write("Dimension 3\n")
        fp.write("SolAtVertices\n")
        fp.write(str(len(verts)))
        fp.write("\n1 1\n") 

        #Compute colors
        if(len(vgrp)>0):
            GROUP = bpy.context.active_object.vertex_groups.active
            cols = [1.0] * len(verts)
            for i,t in enumerate(triangles):
                for j,v in enumerate(t.vertices):
                    try:
                        cols[v] = float(1.0 - GROUP.weight(v))
                    except:
                        continue#cols[v] = 1.0
            for c in cols:
                fp.write('%.8f' % (hmin + c * (hmax-hmin)))
                fp.write("\n")
        fp.close()

    return {'FINISHED'}


if __name__ == "__main__":
    register()
