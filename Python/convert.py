# .obj to .mesh conversion
def obj2mesh(inFile, outFile):
    inp = open(inFile, "r")
    out = open(outFile, "w")

    LINES = inp.readlines()
    inp.close()

    inds = [l.split()[0] for l in LINES]
    nV = len([x for x in inds if x == "v"])
    nT = len([x for x in inds if x == "f"])

    out.write("MeshVersionFormatted 2\nDimension 3\n\n")
    out.write("Vertices\n"+str(nV)+"\n")
    for i,l in enumerate(LINES):
        if (inds[i]=="v"):
            out.write(" ".join([l.split()[i] for i in range(1,4)]) + " 1\n")

    out.write("\nTriangles\n"+str(nT)+"\n")
    for i,l in enumerate(LINES):
        if (inds[i]=="f"):
            out.write(" ".join([str(int(l.split()[i])) for i in range(1,4)]) + " 1\n")

    out.close()
    print "Successfully converted " + inFile

# .stl to .mesh conversion
def stl2mesh(inFile, outFile):
    inp = open(inFile, "r")
    out = open(outFile, "w")

    LINES = inp.readlines()
    nV = nT = 0
    for l in LINES:
        if(l.split()[0] == "facet"):
            nT+=1
    nV = 3 * nT
    inp.close()

    out.write("MeshVersionFormatted 2\nDimension 3\n\n")

    out.write("Vertices\n"+str(nV)+"\n")
    for l in LINES:
        if (l.split()[0]=="vertex"):
            out.write(" ".join([l.split()[i] for i in range(1,4)]) + " 1\n")

    out.write("\nTriangles\n"+str(nT)+"\n")
    cur = 1;
    for l in LINES:
        if (l.split()[0]=="facet"):
            out.write(" ".join([str(cur+i) for i in range(3)]) + " 1\n")
            cur+=3

    out.close()
    print "Successfully converted " + inFile

# .mesh to .obj conversion
def mesh2obj(infile, outfile):

    inp = open(infile, "r")
    out = open(outfile, "w")

    vFound = tFound = False
    vBegin = tBegin = 0
    nV = nT = 0

    LINES = inp.readlines()
    inp.close()

    out.write("o " + infile.split(".")[0] + "\n")

    for i,l in enumerate(LINES):

        s = l.split()

        if vFound and i >= vBegin and i < vBegin + nV:
            out.write("v " + s[0] + " " + s[1] + " " + s[2] + "\n")
        if tFound and i >= tBegin and i < tBegin + nT:
            out.write("f " + s[0] + " " + s[1] + " " + s[2] + "\n")

        if("ert" in l):
            vBegin = i+2
            vFound = True
            nV = int(LINES[i+1])
        if("riang" in l):
            tBegin = i+2
            tFound = True
            nT = int(LINES[i+1])

    out.close()
    print outfile + " correctly written"

# .mesh to .stl conversion
def mesh2stl(infile, outfile):
    inp = open(infile, "r")
    out = open(outfile, "w")
    vFound = tFound = False
    vBegin = tBegin = 0
    nV = nT = 0
    LINES = inp.readlines()
    inp.close()
    
    for i,l in enumerate(LINES):
        if vFound:
            nV = int(l)
            vFound = False
        if("ert" in l):
            vBegin = i+2
            vFound = True

        if tFound:
            nT = int(l.split()[0])
            tFound = False
        if("riang" in l):
            tBegin = i+2
            tFound = True

    verts = [ [str(v) for v in l.split()[:3]] 
             for i,l in enumerate(LINES)
             if i >= vBegin and i < vBegin + nV ]
    tris  = [ [int(t)-1 for t in l.split()[:3]] 
             for i,l in enumerate(LINES)
             if i >= tBegin and i < tBegin + nT ]

    f = open(outfile, 'w')
    f.write("solid " + outfile.split(".")[0] + "\n")
    for t in tris:
        #tN = np.mean([t.vertex1.normal, t.vertex2.normal, t.vertex3.normal], axis=0)
        f.write("facet normal " + str(1) + " " + str(1) + " " + str(1) + "\n")
        f.write("   outer loop\n")
        f.write("     vertex " + verts[t[0]][0] + " " + verts[t[0]][1] + " " + verts[t[0]][2] + "\n" +
                "     vertex " + verts[t[1]][0] + " " + verts[t[1]][1] + " " + verts[t[1]][2] + "\n" +
                "     vertex " + verts[t[2]][0] + " " + verts[t[2]][1] + " " + verts[t[2]][2] + "\n")
        f.write("   endloop\n")
        f.write("endfacet\n")
    f.write("end solid")
    f.close()
    print outfile + " correctly written"



# Conversion wrapper
def convert(i, o):

    inpExt = i.split(".")[-1]
    outExt = o.split(".")[-1]

    if inpExt == "mesh":
        if outExt == "stl":
            mesh2stl(i,o)
        elif outExt == "obj":
            mesh2obj(i,o)
        else:
            print "Non valid output extension: " + outExt

    elif inpExt == "obj":
        if outExt == "mesh":
            obj2mesh(i,o)
        else:
            print "Non valid output extension: " + outExt

    elif inpExt == "stl":
        if outExt == "mesh":
            stl2mesh(i,o)
        else:
            print "Non valid output extension: " + outExt

    else:
        print "Non valid input extension: " + inpExt



# Main execution
if __name__ == '__main__':
    import parsing
    import os
    import sys

    #Create an arguments parser
    description = "Converts files from and to mesh, stl and obj formats. Use either with -iDir, -oDir, -iExt and -oExt arguments to convert all files from a directory, or -i and -o arguments to convert a specific file."
    PARSER = parsing.parser(description)
    options = [("-iDir", "input directory",                 str),
               ("-oDir", "output directory",                str),
               ("-iExt", "input format ( stl, mesh, obj)",  str),
               ("-oExt", "output format ( stl, mesh, obj)", str),
               ("-i",    "input .mesh file",                str),
               ("-o",    "output .stl file",                str)]
    for opt in options:
        PARSER.add_argument( opt[0], opt[1], opt[2] )
    ARGS = PARSER.parse_args()

    #Post-processes the arguments and selects the case
    usage = None
    if ARGS.i != None and ARGS.o != None and ARGS.iDir == None and ARGS.oDir == None and ARGS.iExt == None and ARGS.oExt == None:
        usage = "file"
    elif ARGS.i == None and ARGS.o == None and ARGS.iDir != None and ARGS.oDir != None and ARGS.iExt != None and ARGS.oExt != None:
        usage = "directory"
    else:
        usage = "wrong"

    #Convert a single file
    if usage == "file":
        convert(ARGS.i, ARGS.o)
        sys.exit()

    #Convert a all files from a directory to another
    elif usage == "directory":
        files = [f 
                 for f in os.listdir(ARGS.iDir) 
                 if "." + ARGS.iExt in f and f[0] != "."]
        for f in files:
            if(ARGS.oDir == None):
                convert(ARGS.iDir + f, ARGS.iDir + f[:-len(ARGS.iExt)] + ARGS.oExt)
            else:
                convert(ARGS.iDir + f, ARGS.oDir + f[:-len(ARGS.iExt)] + ARGS.oExt)
        sys.exit()

    elif usage == "wrong":
        PARSER.print_help()
        sys.exit()
