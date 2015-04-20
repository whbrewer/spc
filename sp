#!/usr/bin/env python
import sys, os, shutil, urllib2
if os.path.exists("scipaas/config.py"):
    from scipaas import config, uploads
    from scipaas import apps as appmod
import xml.etree.ElementTree as ET
import hashlib, re

sys.argv[1:]

url = 'https://s3-us-west-1.amazonaws.com/scihub'

def usage():
    buf =  "SciPaaS usage: sp <command> [options]\n\n"
    buf += "available commands:\n"
    buf += "go       start the server\n"
    buf += "init     initialize a database for scipaas\n"
    buf += "install  install an app\n"
    buf += "list     list installed or available apps\n"
    buf += "search   search for available apps\n"
    buf += "test     run unit tests\n"
    return buf

if (len(sys.argv) == 1):
    print usage()
    sys.exit()

#db = config.db

def create_config_file():
    """Create a config.py file in the SciPaaS directory"""
    fn="scipaas/config.py"
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            f.write("db = 'scipaas.db'\n")
            f.write("dbdir = 'db'\n")
            f.write("uri = 'sqlite://'+db\n")
            f.write("apps_dir = 'apps'\n")
            f.write("user_dir = 'user_data'\n")
            f.write("upload_dir = '_uploads'\n")
            f.write("tmp_dir = 'static/tmp'\n")
            f.write("mpirun = '/usr/local/bin/mpirun'\n")
            f.write("# scheduler options\n")
            f.write("# uniprocessor scheduling -- for single-core machines\n")
            f.write("sched = 'uni'\n")
            f.write("# schedule more than one job at a time (multiprocessor)\n")
            f.write("#sched = 'smp'\n")
            f.write("# number of processors available to use on this machine\n")
            f.write("np = 2\n")
            f.write("# don't define server if you want to use built-in\n")
            f.write("# other options: cherrypy, bjoern, tornado, gae, etc.\n")
            f.write("# cherrypy is a decent multi-threaded server\n")
            f.write("#server = 'cherrypy'\n")


def initdb():
    """Initializes database file"""
    from scipaas import config
    from scipaas import model2
    # somehow the following doesn't work properly

    # create db directory if it doesn't exist
    if not os.path.exists(config.dbdir):
        os.makedirs(config.dbdir)
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
    #dal.db.disciplines.insert(name="Chemistry")
    #dal.db.disciplines.insert(name="Linguistics")
    #dal.db.disciplines.insert(name="Finance")
    #dal.db.disciplines.insert(name="Biology")
    #dal.db.disciplines.insert(name="Physics")
    #dal.db.disciplines.insert(name="Fluid Dynamics")
    #dal.db.disciplines.insert(name="Geodynamics")
    #dal.db.disciplines.insert(name="Molecular Dynamics")
    #dal.db.disciplines.insert(name="Weather Prediction")
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
        create_config_file()
        print "creating database."
        initdb()
    elif (sys.argv[1] == "go"):
        os.system("python scipaas/main.py")
    elif (sys.argv[1] == "search"):
        print notyet
    elif (sys.argv[1] == "test"):
        os.chdir('tests')  
        os.system("python test_unit.py")
    elif (sys.argv[1] == "install"):
        install_usage = "usage: sp install appname [--local]"
                
        if 3 <= len(sys.argv) <= 4:

            os.chdir(config.apps_dir)

            # to install local zip file sitting in apps dir
            # sp install xyz --local
            if len(sys.argv) < 4:
                # download zip file into apps folder
                durl = url+'/'+sys.argv[2]+'.zip' 
                print 'durl is:',durl
                dlfile(durl)

            save_path = sys.argv[2]
            print "save_path:", save_path
            if os.path.isfile(save_path):
                print 'ERROR: zip file exists already. Please remove first.'
                sys.exit()

            import zipfile
            # unzip file
            fh = open(save_path+".zip", 'rb')
            z = zipfile.ZipFile(fh)
            z.extractall()
            fh.close()

            # read the json app config file and insert info into db
            import json
            from scipaas import model2
            # future here: unzip file
            app = sys.argv[2]
            path = app + os.sep + app + ".json"
            print path
            with open(path,'r') as f: 
                data = f.read()
            print data
            parsed = json.loads(data)
            print parsed
            
            # copy tpl file to views/apps folder
            src = app + os.sep + app + '.tpl'
            dst = os.pardir + os.sep + 'views' + os.sep + 'apps'
            shutil.copy(src,dst)
            # copy input file--don't need b/c file is already in apps folder
            #if parsed['input_format'] == "namelist":
            #    path = app + os.sep + app + ".in"
            #else if parsed['input_format'] == "ini":
            #    path = app + os.sep + app + ".ini"
            #else if parsed['input_format'] == "xml":
            #    path = app + os.sep + app + ".xml"
            #else:
            #    print "ERROR: input format not supported"
            #    sys.exit()

            # add app to database
            os.chdir(os.pardir)
            dal = model2.dal(uri=config.uri,migrate=True)
            dal.db.apps.insert(name=parsed['name'],
                               description=parsed['description'],
                               category=parsed['category'],
                               language=parsed['language'],
                               input_format=parsed['input_format'],
                               command=parsed['command'])
            dal.db.commit()
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

