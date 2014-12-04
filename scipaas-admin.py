#!/usr/bin/env python

import apps
import sys, os, shutil
import macaron 
import config
from models import * 

sys.argv[1:]
usage = "usage: " + sys.argv[0] + " create appname"

#if (len(sys.argv) < 3):
#    print usage
#    sys.exit()

def initdb():
    """Initializes database file"""
    import hashlib

    db = config.db
    # make a backup copy if file exists
    if os.path.isfile(db): 
        shutil.copyfile(db, db+".bak")

    # Initializes Macaron
    macaron.macaronage(db)

    # Creates tables
    SQL_T_APPS = """CREATE TABLE IF NOT EXISTS apps(
        appid integer primary key autoincrement, 
        name varchar(20), description varchar(80), category varchar(20), 
        language varchar(20), input_format)"""

    SQL_T_USERS = """CREATE TABLE IF NOT EXISTS users(
        uid integer primary key autoincrement, user varchar(20), 
        passwd varchar(20))"""

    SQL_T_JOBS = """CREATE TABLE IF NOT EXISTS jobs(
        jid integer primary key autoincrement, user text, app text,
        cid text, state char(1), time_submit text, description text)"""

    SQL_T_PLOTS = """CREATE TABLE IF NOT EXISTS plots(
        pltid integer primary key autoincrement, 
        appid integer,  type varchar(80), filename varchar(80), col1 integer, col2 integer, 
        title varchar(80), foreign key (appid) references apps(appid))"""

    macaron.execute(SQL_T_USERS)
    macaron.execute(SQL_T_JOBS)
    macaron.execute(SQL_T_APPS)
    macaron.execute(SQL_T_PLOTS)

    # create a default user/pass as guest/guest
    user = "guest"
    pw = "guest"
    hashpw = hashlib.sha256(pw).hexdigest()

    u = Users.create(user=user, passwd=hashpw)
    a = Apps.create(name="dna",description="Compute reverse complement, GC content, and codon analysis of given DNA string.",
        category="bioinformatics",language="python",input_format="namelist")
    macaron.bake()

if(sys.argv[1] == "create"):
    if sys.argv[2]: 
        #myapp = apps.namelist(sys.argv[2])
        myapp = apps.ini(sys.argv[2])
    params,_,_ = myapp.read_params()
    if myapp.write_html_template():
        print "successfully output template"
elif (sys.argv[1] == "init"):
    initdb()
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
