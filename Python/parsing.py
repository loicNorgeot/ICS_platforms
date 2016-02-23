# coding: utf-8 

import argparse
import os

class parser:
    def __init__(self, desc=None):
        self.parser = argparse.ArgumentParser(description=desc)
    def add_argument(self, _flag, _help, _type):
        if(_type == None):
            self.parser.add_argument(_flag,
                                     action="store_true",
                                     help=_help)
        else:
            self.parser.add_argument(_flag,
                                     action="store",
                                     type=_type,
                                     help=_help)
    def print_help(self):
        self.parser.print_help()
    def parse_args(self):
        return self.parser.parse_args()

def command(programName, parsedArgs):
    cmd = programName
    for a in vars(parsedArgs):
        val = getattr(parsedArgs, a)
        if(val != None):
            if(val == True):
                cmd += " -" + a
            elif(val != False):
                cmd += " -" + a + " " + str(val)
    os.system(cmd)
