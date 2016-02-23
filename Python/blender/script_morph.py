# coding: utf8
import bpy
import sys
import os
sys.path.append("/home/loic/Bureau/pymesh/blender/")
import meshes

def readMesh(file):
    file = os.fsencode(file)
    with open(file, 'r') as f:
        verts = []
        triangles = []
        nV = 0
        nT = 0
        readVertices = False
        readTriangles = False
        iV = iT = 0

        REFS = []

        for line in f:
            #Vertices reading
            if (readVertices and (nV>0)):
                if(iV<nV):
                    try:
                        px, py, pz = [float(x) for x in line.split()[:3]]
                        iV += 1
                        verts.append((px, py, pz))
                    except ValueError:
                        pass
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
                    if(r not in REFS):
                        REFS.append(r)
                        triangles.append([])
                    for i,ref in enumerate(REFS):
                        if r == ref:
                            triangles[i].append((px, py, pz,r))
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

    return verts, triangles, REFS

def importMesh(filename):
    # Assemble mesh
    verts, triangles, refs = readMesh(filename)
    for t,r in zip(triangles, refs):
        mesh_name = filename.split("/")[-1].split(".")[0] + "." + str(r)
        print(mesh_name)
        mesh = bpy.data.meshes.new(name=mesh_name)
        mesh.from_pydata(verts, [], [tr[:3] for tr in t])
        mesh.validate()
        mesh.update()

        scene = bpy.context.scene
        obj = bpy.data.objects.new(mesh.name, mesh)
        scene.objects.link(obj)
        scene.objects.active = obj
        obj.select = True
        #obj.matrix_world = global_matrix

        scene.update()
    


if __name__ == "__main__":
    directory = "/home/loic/Téléchargements/"
    files     = [f for f in os.listdir(directory) if "ChaclaTotal" in f and ".mesh" in f]
    files.sort()

    bpy.ops.object.delete()

    importMesh(directory + files[0])

    print(files)

    for f in files:
        verts, triangles, refs = readMesh(directory + f)
        for basis in bpy.context.scene.objects:
            basis.select=True
            if basis.type == "MESH":
                shapeKey = basis.shape_key_add(from_mix=False)
                shapeKey.name = "1"
                for vert, newV in zip(basis.data.vertices, verts):
                    shapeKey.data[vert.index].co = newV
                    #print(vert.co)  # this is a vertex coord of the mes
            basis.select=False

    for basis in bpy.context.scene.objects:
        if basis.type == "MESH":
            nb = len(files)
            scene = bpy.context.scene
            scene.frame_start = 1
            scene.frame_end   = 1 + nb * 5

            for i in range(nb):
            #bpy.ops.anim.change_frame(frame = 1 + 10*nb)
                for j,key in enumerate(basis.data.shape_keys.key_blocks):
                    if i == j:
                        key.value = 1
                    else:
                        key.value = 0
                    key.keyframe_insert("value", frame=1 + 5*i)
