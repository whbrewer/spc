#!/usr/bin/env python

import apps
import sys
import os

sys.argv[1:]
usage = "usage: sys.argv[0] create appname"

if (len(sys.argv) < 3):
    print usage
    sys.exit()

if(sys.argv[1] == "create"):
    if sys.argv[2]: 
        #myapp = apps.namelist(sys.argv[2])
        myapp = apps.ini(sys.argv[2])
    params,_,_ = myapp.read_params()
    if myapp.write_html_template():
        print "successfully output template"
else:
    print usage

#try:
#    if(sys.argv[1] == "n"):
        #if sys.argv[2]: 
        #myapp = apps.namelist(argv[2])
#        myapp = apps.namelist('burger')
#        params = myapp.read_params()
#        if myapp.write_html_template():
#		    print "successfully output template"

#    else:
#        print "%s not supported" % sys.argv[1]

#    if(sys.argv[1] == "s"):
#        os.system("python main.py")

#except:
#    print "usage: " + sys.argv[0] + " <command>"
#    print
#    print "list of commands:"
#    print "n - create new project"
#    print "s - start the web server"
