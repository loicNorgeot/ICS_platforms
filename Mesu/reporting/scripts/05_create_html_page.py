import os
from parsing import *

def init_arguments():
    PARSER = parser("Get MeSU servers usage information")
    options = [option("-directory", "files directory", str)]
    for opt in options:
        PARSER.add_argument( opt )
    return PARSER

#Balises html 
def h1(x):
	return "<h1>" + x + "</h1>"
def h2(x):
        return "<h2>" + x + "</h2>"
def a(link,x):
	return '<a href="' + link + '">' + x + "</a>"
def p(x):
	return "<p>" + x + "</p>"

#main
if __name__=="__main__":
	parser = init_arguments()
	args   = parser.parse_args()
	if(args.directory):
		path = args.directory + "/"
		with open(path+"index.html","w") as file:
			ignore = ["~"]
			files = os.listdir(path)
			files = [f for f in files if "txt" in f or "csv" in f]
			files.sort()
			file.write(h1("Usage data for MeSU")+"\n")
			
			for f in files:
				file.write(p(a(f, f)) + "\n")
	else:
		print "Please specify a directory"
		parser.print_help()
		sys.exit()
