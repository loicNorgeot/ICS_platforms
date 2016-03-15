import os
from parsing import *

def init_arguments():
    PARSER = parser("Create files linking each user with its laboratory")
    options = [option("-affectations",  "affectation output file", str),
               option("-labos",         "labos output file",       str)]
    for opt in options:
        PARSER.add_argument( opt )
    return PARSER

def getUsers(homeDirectory = "/home/", database="/opt/dev/pbs/spool/server_priv/bdd.pbs.sqlite3"):
    users = []
    
    # pbs database:
    os.system("sqlite3 " + database + " \"SELECT distinct(user) FROM pbs_jobs;\" > tmp_users.txt")
    with open("tmp_users.txt","r") as f:
        for l in f.readlines():
            user = l[:-1]
            os.system("ldapsearch -y /root/ics/reporting/.mdp.txt -x -h 134.157.146.25 uid="+user+" | grep uidInterne: > tmp_user.txt")
            new = open("tmp_user.txt","r").readlines()
            if len(new)>0:
                user = new[0].split()[1]
            users.append(user)
            os.remove("tmp_user.txt")
    os.remove("tmp_users.txt")

    # home directory
    homes = os.listdir(homeDirectory)
    for h in homes:
        if h not in users:
            users.append(h)

    users.sort()

    #Keeping uidInterne only (full name)
    rm=[]
    for i,u in enumerate(users[:-1]):
        if u==users[i+1][:11]:
            rm.append(i)
    for i in rm[::-1]:
        users.remove(users[i])

    return users

def getLabs(names):
    labs=[]
    for user in names:
        os.system("ldapsearch -y /root/ics/reporting/.mdp.txt -h 134.157.146.25 uidInterne=" + user + "	-x | grep ffectation > tmp_affectation.txt")
        L = open("tmp_affectation.txt","r").readlines()
        affectation = "0"
        principale=0
        for l in L:
            if "affectationPrincipale" in l:
                affectation = l.split("ou=")[1][:-1]
                principale = 1
        for l in L:
            if not principale:
                if "supannAffectation" in l:
                    affectation=l.split("ou=")[1][:-1]
                    principale=1
        #if not principale:
        #    print "affectation not found for " + user
        labs.append(affectation)
        os.remove("tmp_affectation.txt")
    return labs
    
def createLabs(labos):
    labos = set(labos)
    names=[]
    for l in labos:
        os.system("ldapsearch -y /root/ics/reporting/.mdp.txt -h 134.157.146.25 ou=" + l + " -x > tmp_labo.txt")
        L = open("tmp_labo.txt","r").readlines()
        name = "Not found"
        principale=0
        try:
            for l in L:
                if "sigleAbrege" in l:
                    name = l.split("sigleAbrege: ")[1][:-1]
                    principale = 1
            
            for l in L:
                if not principale:
                    if "description: " in l:
                        name=l.split("description: ")[1][:-1]
                        principale=1
        except:
            name="Not Found"
        names.append(name)
        os.remove("tmp_labo.txt")
    return list(labos), names

if __name__=="__main__":
    parser = init_arguments()
    args   = parser.parse_args()

    users = getUsers()
    labs = getLabs(users)
    
    if(args.affectations):
        with open(args.affectations,"w") as f:
            for u,l in zip(users, labs):
                f.write(u + "," + l + ",\n")
    if(args.labos):
        LABOS, NAMES = createLabs(labs)
        R = [x for x in sorted(zip(LABOS, NAMES))]
        with open(args.labos,"w") as f:
            for r in R:
                f.write(r[0]+","+r[1]+",\n")
    
    


    

"""
# 1 - Create the list of all users (from pbs database and from /users directory)
USERS = []

# 1.1 - /home directories
homes = []

with open("final.csv","w") as result:
    userFiles = [f for f in os.listdir("./") if "0_" in f]
    print "Found "+str(len(userFiles))+" users."
    AFFS = []
    for userFile in userFiles:
        L = open(userFile,"r").readlines()
        affectations = []
        principale=0
        for l in L:
            if "affectationPrincipale" in l:
                AFFS.append((userFile[2:-4],l.split("ou=")[1][:-1]))
                principale = 1
        if not principale:
            for l in L:
                if "supannAffectation" in l:
                    AFFS.append((userFile[2:-4],l.split("ou=")[1][:-1]))
                    principale=1
        if not principale:
            print "affectation not found for " + userFile

    for a in AFFS:
        result.write(a[0]+','+a[1]+',\n')
"""
