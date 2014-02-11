#!/usr/bin/env python
import sqlite3 as lite
import threading
import config
import time

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
            print "scheduler:", self.qstat(), "jobs in queued state"
            #if(self.qstat() > 0):
            #    continue
            time.sleep(5) 

    def qsub(self,appid,cid):
        cur = self.con.cursor()
        cmd = 'insert into jobs values (null, ?, ?, ?, ?);'
        state = 'Q'
        cur.execute(cmd,(appid,cid,state,time.asctime())) 
        self.con.commit()

    def qfront(self):
        cur = self.con.cursor()
        cmd = "select jid from jobs where state = 'Q' limit 1"
        (jid) = cur.execute(cmd).fetchone()
        return jid

    #def last(self):
    #    cur = self.con.cursor()
    #    return cur.lastrowid

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
        connector = lite.connect(config.database)
        cmd = 'select name,cid from apps natural join jobs where jid=?'
        c = db.execute(cmd,(jid,))
        [(app,cid)] = c.fetchall()
        print 'result:',app,cid
        rel_path=(os.pardir+os.sep)*4
        run_dir = myapps[app].user_dir + os.sep + user + os.sep + myapps[app].appname + os.sep + cid
        print 'run_dir:',run_dir
        cmd = rel_path + myapps[app].exe + " > " + myapps[app].outfn
        print "cmd:",cmd
        os.system("cd " + run_dir + ";" + cmd + " &")
        #sched.qdel(jid)
        cmd = "update jobs set state = 'R' where jid=?"
        c = db.execute(cmd,(jid,))
        c.close()
        redirect("/"+app+"/"+cid+"/monitor")

    def stop(self):
        pass

    def __allocate(self):
        pass
    
    def __terminate(self):
        pass

#if __name__ == "__main__":
#    sched = scheduler()
#    sched.qsub('test')
#    print 'top row id:', sched.qpop()

#if __name__ == "__main__":
#    sched = scheduler()
#    hw_thread = threading.Thread(target = assignTask)
#    hw_thread.daemon = True
#    hw_thread.start()
#    try:
#        time.sleep(500000)
#
#    except KeyboardInterrupt:
#        print '\nGoodbye!'
