import os
from parsing import *
from random import shuffle

def init_arguments():
    PARSER = parser("Create files linking each user with its laboratory")
    options = [option("-affectations",  "affectation input file", str),
               option("-labos",         "labos input file",       str),
               option("-i",             "input statistics file",  str),
               option("-o",             "output csv file",        str)]
    for opt in options:
        PARSER.add_argument( opt )
    return PARSER

class user:
    def __init__(self, values):
        self.name    = values[0]
        self.labID   = values[1]
        self.hours   = values[2][:-2]
        self.labName = ""

def get_users_statistics(filename):
    with open(filename,"r") as f:
        L = f.readlines()
        return [user(l.split(",")) for l in L]

def update_users_affectations(users, affectation_file):
    affectations = []
    with open(affectation_file, "r") as f:
        L = f.readlines()
        for u in users:
            for l in L:
                if u.name == l[0]:
                    u.labID = l[1]
        return users

def update_users_labs_names(users, filename):
    with open(filename,"r") as f:
        L = [l.split(",") for l in f.readlines()]
        for u in users:
            for l in L:
                if u.labID == l[0]:
                    if "total_users" in args.i:
                        print l[1]
                    u.labName = l[1]
        return users

def write_csv(users, filename):
    contained = ["Institut Du Calcul", "7238", "Affectation", "927",     "925",     "7371",        "7138",           "Not found", "Microbiennes", "Equipe 4"]
    replaces =  ["ICS",                "LCQB", "Partenaires", "UFR 927", "UFR 925", "Imagerie Bio","Evolution Seine","Divers",    "LBBM",         "Institut de myologie"]
    for u in users:
        for c,r in zip(contained, replaces):
            if c in u.labName:
                u.labName=r
        if u.labName=="":
            u.labName="Divers"
    with open(filename,"w") as f:
        f.write("user,labo,hours,\n")
        for u in users:
            f.write(u.name+","+u.labName+","+u.hours+",\n")
    with open(filename[:-4]+"_shuffled.csv","w") as f:
        f.write("user,labo,hours,\n")
        shuffle(users)
        for u in users:
            f.write(u.name+","+u.labName+","+u.hours+",\n")

if __name__=="__main__":
    parser = init_arguments()
    args   = parser.parse_args()

    if not args.affectations or not args.labos or not args.i or not args.o:
        parser.print_help()
        sys.exit()
    else:
        USERS = get_users_statistics(args.i)
        USERS = update_users_affectations(USERS, args.affectations)
        USERS = update_users_labs_names(USERS, args.labos)
        write_csv(USERS, args.o)
            
