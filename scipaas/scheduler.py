#!/usr/bin/env python
import sqlite3 as lite
import threading, time, os
import config
from dal import DAL, Field

#inspired from:
#http://taher-zadeh.com/a-simple-and-dirty-batch-job-scheduler-daemon-in-python/

db2 = DAL('sqlite://scipaas.db', auto_import=True, migrate=False)

jobs = db2.define_table('jobs', Field('id','integer'),
                                Field('user','string'),
                                Field('app','string'),
                                Field('cid','string'),
                                Field('state','string'),
                                Field('time_submit','string'),
                                Field('description','string'))

class scheduler(object):

    def __init__(self):
        # Connect to DB 
        self.con = None
        try: 
            self.con = lite.connect(config.db)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        # start polling thread
        t = threading.Thread(target = self.assignTask)
        t.daemon = True
        t.start()

    def assignTask(self):
        while(True):
            #print "scheduler:", self.qstat(), "jobs in queued state", 
            #time.asctime()
            j = self.qfront()
            if j is not None and j > 0:
                self.start(j)            
            time.sleep(5) 

    def qsub(self,app,cid,user):
        cur = self.con.cursor()
        query = 'insert into jobs values (null, ?, ?, ?, ?, ?, ?);'
        state = 'Q'
        description = 'none'
        cur.execute(query,(user,app,cid,state,time.asctime(),description)) 
        self.con.commit()

    def qfront(self):
        self.connector = lite.connect(config.db)
        cur = self.connector.cursor()
        query = "select id from jobs where state = 'Q' limit 1"
        (jid) = cur.execute(query).fetchone()
        self.connector.close()
        if jid is not None:
            return jid[0]
        else:
            return -1

    def qdel(self,jid):
        cur = self.con.cursor()
        cur.execute('delete from jobs where id = ?', (jid,))
        self.con.commit()
        return 1

    def qstat(self):
        try: 
            self.connector = lite.connect(config.db)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        cur = self.connector.cursor()
        query = "Select count(id) from jobs where state='Q'"
        cur.execute(query)
        c = cur.fetchone()
        self.connector.close()
        return c[0]

    def start(self,jid):
        global myapps
        connector = lite.connect(config.db)
        query = "update jobs set state = 'R' where id=?"
        c = connector.execute(query,(jid,))
        connector.commit()

        query = 'select user,app,cid from jobs where id=?'
        c = connector.execute(query,(jid,))
        [(user,app,cid)] = c.fetchall()
        rel_path=(os.pardir+os.sep)*4
        run_dir = config.user_dir + os.sep + user + os.sep + app + os.sep + cid
        exe = config.apps_dir + os.sep + app + os.sep + app
        outfn = app + ".out"
        cmd = rel_path + exe + " " + app + ".ini >& " + outfn
        t = threading.Thread(target = self.start_job(run_dir,cmd))
        t.start()

        query = "update jobs set state = 'C' where id=?"
        connector.execute(query, (jid,))
        connector.commit()
        c.close()

    def start_job(self,run_dir,cmd):
        print 'starting thread to run job:',run_dir, cmd
        os.system("cd " + run_dir + ";" + cmd )

    def stop(self,app):
        os.system("killall " + app)
