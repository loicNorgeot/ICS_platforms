import sqlite3
import csv
import sys
import time

from parsing import *

def init_arguments():
    PARSER = parser("Get MeSU servers usage information")

    options = [option("-b", "start time", str),
               option("-e", "end   time", str),
               option("-last", "Either 'hour', 'day', 'week', 'month', 'year' or 'total'", str),

               option("-o", "output file",   str),
               option("-i", "write header",  None),
               option("-p", "print results", None),

               option("-user",  "user name",  str),
               option("-labo",  "labo name",  str),
               option("-queue", "queue name", str),

               option("-users",   "list users",  None),
               option("-labos",   "list labos",  None),
               option("-queues",  "list queues", None),
               option("-globals", "global stats",None)]

    for opt in options:
        PARSER.add_argument( opt )

    return PARSER

def init_db(filename):
    connection = sqlite3.connect(filename)
    cursor     = connection.cursor()
    return cursor

if __name__=="__main__":
    parser = init_arguments()
    args   = parser.parse_args()
    cursor = init_db('/opt/dev/pbs/spool/server_priv/bdd.pbs.sqlite3')

    header, query = None, None
    start         = "0"
    output        = "result.txt" if not args.o else args.o


    if args.last:
        t = int(time.time())
        durations = [("hour",3600),("day",24*3600),("week",24*7*3600),("month",24*30*3600),("year",24*3600*365.25), ("total",24*3600*365.25*10)]
        for d in durations:
            if args.last==d[0]:
                start = str(t - d[1])
        if start == "0":
            print "Incorrect value for 'last', starting from the beginning"

    if args.users:
        query  = "select user,labo,sum(Ucput)/3600 from pbs_jobs where start>"+start+" group by user order by sum(Ucput) DESC"
        header = ["User","Labo","Cpu time (h)"]
        #output = "users.csv"
    elif args.labos:
        query  = "select labo, sum(Ucput)/3600 from pbs_jobs where start>"+start+" group by labo order by sum(Ucput) DESC"
        header = ["Labo","Cpu time (h)"]
        #output = "labos.csv"
    elif args.queues:
        query  = "select queue,sum(Ucput)/3600 from pbs_jobs where start>"+start+" group by queue order by sum(Ucput) DESC"
        header = ["Queue","Cpu time (h)"]
        #output = "queues.csv"
    elif args.user:
        query  = 'select jobid, queue, jobname, ncpus, Ucpupercent, Ucput/3600 from pbs_jobs where user="' + args.user + '" and start>'+start+' order by Ucput DESC'
        header = ["Job ID", "Queue", "Job name", "Requested CPUs", "Cpu usage", "Cpu time (h)"]
        #output = "user_" + args.user + ".csv"
    elif args.labo:
        query  = 'select user,sum(Ucput)/3600 from pbs_jobs group by user where labo="' + args.labo + '" and start>'+start+'order by user'
        header = ["User","Cpu time (h)"]
        #output = "labo_" + args.labo + ".csv"
    elif args.queue:
        query  = 'select queue, sum(Ucput)/3600 from pbs_jobs where queue="' + args.queue + '" and start>'+start
        header = ["Queue", "Cpu time (h)"]
        #output="queue_" + args.queue + ".csv"
    elif args.globals:
        query  = 'select sum(Ucput)/3600 from pbs_jobs where start>'+start
        header = ["Cpu time (h)"]
    if not query:
        print "No query, please specify an argument"
        parser.print_help()
        sys.exit()

    result = cursor.execute(query)

    if args.p:
        for r in result:
            print r
    else:
        
        with open(output, 'w') as f:
            writer = csv.writer(f)
            if args.i:
                writer.writerow(header)
            writer.writerows(result)
