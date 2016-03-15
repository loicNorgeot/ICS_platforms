import argparse
import sys

class parser:
    def __init__(self, desc=None):
        self.parser = argparse.ArgumentParser(description=desc)
    def add_argument(self, opt):
        if(opt.type == None):
            self.parser.add_argument(opt.flag,
                                     action="store_true",
                                     help=opt.help,
                                     required=opt.req)
        else:
            self.parser.add_argument(opt.flag,
                                     action="store",
                                     type=opt.type,
                                     help=opt.help,
                                     required=opt.req)
    def print_help(self):
        self.parser.print_help()
    def parse_args(self):
        return self.parser.parse_args()

class option:
    def __init__(self, f, h, t, req=False):
        self.flag = f
        self.help = h
        self.type = t
        self.req  = req

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
