#!/usr/bin/env python
import sqlite3 as lite
import threading
import config
import time
import os

#inspired from:
#http://taher-zadeh.com/a-simple-and-dirty-batch-job-scheduler-daemon-in-python/

#CREATE TABLE jobs (
#jid integer primary key autoincrement,
#appid integer, 
#cid integer,
#state char(1),
#time_submit text 
#);

class scheduler(object):

    def __init__(self):
        # Connect to DB 
        self.con = None
        try: 
            self.con = lite.connect(config.database)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        # start polling thread
        t = threading.Thread(target = self.assignTask)
        t.daemon = True
        t.start()

    def assignTask(self):
        while(True):
            print "scheduler:", self.qstat(), "jobs in queued state",\
                time.asctime()
            j = self.qfront()
            if j is not None and j > 0:
                self.start(j)            
            time.sleep(5) 

    def qsub(self,appid,cid):
        cur = self.con.cursor()
        cmd = 'insert into jobs values (null, ?, ?, ?, ?);'
        state = 'Q'
        cur.execute(cmd,(appid,cid,state,time.asctime())) 
        self.con.commit()

    def qfront(self):
        self.connector = lite.connect(config.database)
        cur = self.connector.cursor()
        cmd = "select jid from jobs where state = 'Q' limit 1"
        (jid) = cur.execute(cmd).fetchone()
        self.connector.close()
        if jid is not None:
            return jid[0]
        else:
            return -1

    def qdel(self,jid):
        print "jid is:",jid
        cur = self.con.cursor()
        cur.execute('delete from jobs where jid = ?', (jid,))
        self.con.commit()
        return 1

    def qstat(self):
        try: 
            self.connector = lite.connect(config.database)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        cur = self.connector.cursor()
        cmd = "Select count(jid) from jobs where state='Q'"
        cur.execute(cmd)
        c = cur.fetchone()
        self.connector.close()
        return c[0]

    def start(self,jid):
        global myapps
        #print 'start:',jid
        connector = lite.connect(config.database)
        cmd = "update jobs set state = 'R' where jid=?"
        c = connector.execute(cmd,(jid,))
        connector.commit()

        cmd = 'select name,cid from apps natural join jobs where jid=?'
        c = connector.execute(cmd,(jid,))
        [(app,cid)] = c.fetchall()
        #print 'result:',app,cid
        rel_path=(os.pardir+os.sep)*4
        user = "guest"
        run_dir = config.user_dir + os.sep + user + os.sep + app + os.sep + cid
        #print 'run_dir:',run_dir
        exe = config.apps_dir + os.sep + app + os.sep + app
        outfn = app + ".out"
        cmd = rel_path + exe + " > " + outfn
        #print "cmd:",cmd
        t = threading.Thread(target = self.start_job(run_dir,cmd))
        t.start()

        connector.execute('delete from jobs where jid = ?', (jid,))
        connector.commit()
        c.close()

    def start_job(self,run_dir,cmd):
        print 'starting thread to run job:',run_dir, cmd
        os.system("cd " + run_dir + ";" + cmd )

    def stop(self):
        pass
