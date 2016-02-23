"""
MMGS_O3 wrapper for mmgs_O3 remeshing tool

Needs the installation of mmgs on the system
Use with mmgs flags: -hmax, -hgrad ... etc.

Two modes are available:
  Single remeshing, same use as mmgs:
    Uses mmgs on a single file, by specifying it.
    Launch with python remesh.py -in inputfile.mesh [-out outputfile.mesh] [mmgs args]
    If no output file is specified, the new file will be inputfile.o.mesh

  Multiple remeshing:
    Remeshes multiple files contained in a directory.
    Launch with python remesh.py -indir inputDir/ [-outdir outputDir] [mmgs args]
    If no output directory is specified, the remeshed files will be located in the input directory and renamed as inputfile.o.mesh

fine
  python pymesh/remesh.py -indir 1_MESH/ -outdir 2_FINE_REMESHING/ -v -nr -hausd 0.000075 -hgrad 1.2 -m 400

coarse
  python pymesh/remesh.py -indir 1_MESH/ -outdir 3_LIGHT_REMESH/ -v -nr -hausd 0.0001 -hgrad 1.2 -m 400

"""
# coding: utf-8 
    
if __name__ == "__main__":
    
    import parsing
    import sys
    import os

    #Create an arguments parser
    PARSER = parsing.parser("Wrapper around mmg")
    options = [("-indir","input directory",str),
               ("-outdir","output directory",str),
               ("-in","input .mesh file", str),
               ("-out","output .mesh file",str),
               ("-hausd","haussdorf distance",float),
               ("-hgrad","gradation",float),
               ("-hmin","minimal edge length",float),
               ("-hmax","maximal edge length",float),
               ("-nr","no angle detection",None),
               ("-m","maximum memory usage",int),
               ("-v","reduced verbosity",None)]
    for opt in options:
        PARSER.add_argument( opt[0], opt[1], opt[2] )
    ARGS = PARSER.parse_args()

    #Remesh multiple files in a directory
    if os.path.isdir(str(ARGS.indir)):
        inDir = str(ARGS.indir)
        outDir = str(ARGS.outdir)
        ARGS.__delattr__("indir")
        ARGS.__delattr__("outdir")
        if(outDir == "None"):
            outDir = inDir
        
        infiles  = [f 
                    for f in os.listdir(inDir) 
                    if f[0]!="." and f.split(".")[-1]=="mesh"]
        outfiles = [".".join([f[:-5],"o","mesh"]) 
                    for f in infiles]
        
        for i,o in zip(infiles, outfiles):
            ARGS.__setattr__("in", inDir  + i)
            ARGS.__setattr__("out",outDir + o)
            parsing.command("mmgs_O3", ARGS)

        sys.exit()

    #Remesh a single file
    else:
        parsing.command("mmgs_O3", ARGS)
        sys.exit()
