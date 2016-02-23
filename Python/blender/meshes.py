import bpy
import os

def import_mesh(file):
    if(".mesh" in file):
        bpy.ops.import_mesh.mesh(filepath = file)
    elif(".stl" in file):
        bpy.ops.import_mesh.stl(filepath = file)
    elif(".ply" in file):
        bpy.ops.import_mesh.ply(filepath = file)
    elif(".obj" in file):
        bpy.ops.import_scene.obj(filepath = file)
    else:
        print("Can't import " + file)
        return 0
def import_all(directory, ext):
    files = [f for f in os.listdir(directory) if ext in f]
    for file in files:
        import_mesh(directory + file)

def export_mesh(file):
    if(".mesh" in file):
        bpy.ops.export_mesh.mesh(filepath = file)
    elif(".stl" in file):
        bpy.ops.export_mesh.stl(filepath = file)
    elif(".ply" in file):
        bpy.ops.export_mesh.ply(filepath = file)
    elif(".obj" in file):
        bpy.ops.export_scene.obj(filepath = file)
    else:
        print("Can't export " + file)
        return 0
def export_all(directory, ext):
    for ob in bpy.context.scene.objects:
        ob.select = False
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            bpy.context.scene.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')  
            file = directory + obj.name + ".o" + ext
            export_mesh(file)
            for ob in bpy.context.scene.objects:
                ob.select = False
            

def replace_all(directory, ext):
    for ob in bpy.context.scene.objects:
        ob.select = False
    notReplaced = []

    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            meshName = ob.name.split(".")[0]
            found = False
            FILES = [f for f in os.listdir(directory) if ext in f]
            bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)
            for f in FILES:
                if f.split(".")[0] == meshName:
                    found = True
                    f = directory + f
                    import_mesh(file=f)
                    bpy.ops.object.origin_set( type = 'GEOMETRY_ORIGIN' )
                    newOb = bpy.context.scene.objects.active

                    newOb.scale          = ob.scale                    
                    newOb.rotation_euler = ob.rotation_euler
                    newOb.location       = ob.location

                    print("Successfully replaced " + ob.name + " by " + f )
                    newOb.select  = False
                    ob.select     = True
                    bpy.ops.object.delete()
                    newOb.name = newOb.name.split(".")[0]
            if not found:
                notReplaced.append(meshName)

    replaced = [f for f in FILES if f not in notReplaced]
    if len(replaced):
        print("\nSuccessfully replaced:")
        for f in FILES:
            if f not in notReplaced:
                print("  " + f)
    if len(notReplaced):
        print("\nCould not replace:")
        for f in notReplaced:
            print("  " + f)


