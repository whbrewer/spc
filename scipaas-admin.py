#!/usr/bin/env python

import apps
import sys
import os

sys.argv[1:]

if(sys.argv[1] == "create"):
    if sys.argv[2]: 
        myapp = apps.app_f90(sys.argv[2])
    params,_,_ = myapp.read_params()
    if myapp.write_html_template():
        print "successfully output template"

#try:
#    if(sys.argv[1] == "n"):
        #if sys.argv[2]: 
        #myapp = apps.app_f90(argv[2])
#        myapp = apps.app_f90('burger')
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