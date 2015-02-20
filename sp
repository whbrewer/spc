#!/usr/bin/env python
from scipaas import config
from scipaas import apps as appmod
#from scipaas.model import *
import sys, os, shutil, urllib2
import xml.etree.ElementTree as ET
import hashlib, re

sys.argv[1:]

url = 'https://s3-us-west-1.amazonaws.com/scihub'

def usage():
    buf =  "SciPaaS usage: sp <command> [options]\n\n"
    buf += "commonly used commands:\n"
    buf += "init     initialize a database for scipaas\n"
    buf += "go       start the server\n"
    buf += "create   create a view template for appname (e.g. sp create myapp)\n"
    buf += "search   search for available apps\n"
    buf += "list     list installed or available apps (e.g. sp list [available|installed]) \n"
    buf += "test     run tests\n"
    buf += "install  install an app\n"
    return buf

if (len(sys.argv) == 1):
    print usage()
    sys.exit()

db = config.db

def initdb():
    """Initializes database file"""
    from scipaas import model2
    # somehow the following doesn't work properly

    # create db directory if it doesn't exist
    #if not os.path.exists(config.dbdir):
    #    os.makedirs(config.dbdir) 
    # make a backup copy of db file if it exists

    #if os.path.isfile(db): 
    #    print "ERROR: a database file already exists, please rename it and rerun"
    #    sys.exit()
    #    shutil.copyfile(db, db+".bak")

    # get rid of old .table files
    for f in os.listdir(config.dbdir):
        if re.search("\.table", f):
            print "removing file:", f
            os.remove(os.path.join(config.dbdir, f))
    # delete previous .db file should back first (future)
    dbpath = os.path.join(config.dbdir, config.db)
    if os.path.isfile(dbpath): os.remove(dbpath)
    # create db
    dal = model2.dal(uri=config.uri,migrate=True)
    # add guest and admin user
    hashpw = hashlib.sha256("guest").hexdigest()
    dal.db.users.insert(user="guest",passwd=hashpw)
    hashpw = hashlib.sha256("admin").hexdigest()
    dal.db.users.insert(user="admin",passwd=hashpw)
    # add default app
    dal.db.apps.insert(name="dna",description="Compute reverse complement," +\
                       "GC content, and codon analysis of given DNA string.", 
                       category="bioinformatics",
                       language="python",  
                       input_format="namelist", 
                       command="../../../../apps/dna/dna")
    dal.db.plots.insert(id=1,appid=1,ptype="flot-cat",title="Dinucleotides")
    dal.db.plots.insert(id=2,appid=1,ptype="flot-cat",title="Nucleotides")
    dal.db.plots.insert(id=3,appid=1,ptype="flot-cat",title="Codons")
    dal.db.datasource.insert(filename="din.out",cols="1:2",pltid=1)
    dal.db.datasource.insert(filename="nucs.out",cols="1:2",pltid=2)
    dal.db.datasource.insert(filename="codons.out",cols="1:2",pltid=3)
    # write changes to db
    dal.db.commit()

notyet = "this feature not yet working"

# http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
def dlfile(url):
    # Open the url
    try:
        f = urllib2.urlopen(url)
        print "downloading " + url
        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
    #handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url

# process command line options
if __name__ == "__main__":
    if (sys.argv[1] == "init"):
        print "creating database " + config.db
        initdb()
    elif (sys.argv[1] == "go"):
        os.system("python scipaas/main.py")
    elif (sys.argv[1] == "search"):
        print notyet
    elif (sys.argv[1] == "test"):
        os.chdir('tests')  
        os.system("python testall.py")
    elif (sys.argv[1] == "install"):
        install_usage = "usage: sp install appname"
        if len(sys.argv) == 3:
            durl = url+'/'+sys.argv[2]+'.zip' 
            print 'durl is:',durl
            dlfile(durl)
        else:
            print install_usage

    elif (sys.argv[1] == "list"):
        list_usage = "usage: sp list [available|installed]"
        if (len(sys.argv) == 3):
            if (sys.argv[2] == "installed"):
                result = Apps.all()
                for r in result:
                    print r.name
            elif (sys.argv[2] == "available"):
                response = urllib2.urlopen(url)
                html = response.read()
                root = ET.fromstring(html)
                for child in root.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
                    for c in child.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Key"):
                        (app,ext) = c.text.split(".")
                        print app 
            else:
                print list_usage
        else:
            print list_usage
    else:
        print "ERROR: option not supported"
        sys.exit()

