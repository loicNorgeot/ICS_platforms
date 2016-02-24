import subprocess

def createDB(output):
    try:
        subprocess.call("pbsacctsql  -b '2016 01 01 00 00 00' -T -S -R > " + output, shell=True)
    except:
        print "Can't execute pbsacctsql"

def updateLabs():
    try:
        subprocess.call("/root/ics/reporting/ldap.sh")
    except:
        print "Can't update Users database"

class stats:
    def __init__(self, line):
        self.user  = line[0]
        self.hours = int(line[2])/3600
        self.labo = line[-1]
    def toString(self):
        return ",".join([self.user, self.labo, str(self.hours)]) + "\n"

def file2Array(fileName):
    F = open(fileName,"r")
    LINES = [l.split() for l in F.readlines()]
    return LINES

def writeCSV(array, fileName):
    F = open(fileName, 'w')
    F.write("User,Labo,hours\n")
    for stat in array:
        if(stat.labo != "none"):
            F.write(stat.toString())
    F.write(",,")

if __name__ == '__main__':
    updateLabs()
    createDB("reporting.txt")
    LINES = file2Array("reporting.txt")
    STATS = [stats(l) for l in LINES[3:-3]]
    writeCSV(STATS, "reporting.csv")

    
    
