import os
from parsing import *

def init_arguments():
    PARSER = parser("Get MeSU servers usage information")
    options = [option("-affectations", "affectations inuput file", str)]
    for opt in options:
        PARSER.add_argument( opt )
    return PARSER

def updateDB(affectationsFile,
             database="/opt/dev/pbs/spool/server_priv/bdd.pbs.sqlite3"):
    with open(affectationsFile,"r") as f:
        L = [l.split(",") for l in f.readlines()]
        for l in L:
            os.system('sqlite3 /opt/dev/pbs/spool/server_priv/bdd.pbs.sqlite3 "UPDATE pbs_jobs SET labo='+l[1]+' WHERE user=\\"'+l[0]+'\\";"')

if __name__=="__main__":
    parser = init_arguments()
    args   = parser.parse_args()
    if(args.affectations):
        updateDB(args.affectations)
    else:
        print "Please specify an affectations file"
        parser.print_help()
        sys.exit()
