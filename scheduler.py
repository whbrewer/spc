#!/usr/bin/env python
import sqlite3 as lite
import threading
import time


#CREATE TABLE jobs ( 
#jid integer primary key autoincrement,
#name varchar(255),
#state char(1),
#time_submit timestamp,
#time_start timestamp,
#time_finish timestamp
#);

class scheduler(object):

    def __init__(self):
        # Connect to DB 
        self.con = None
        try: 
            self.con = lite.connect('scipaas.db')    
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def qsub(self,path):
        cur = self.con.cursor()
        cur.execute('insert into jobs values (null, ?,\'Q\', ?, null, null);',(path,time.time()))
        self.con.commit()

    def qpop(self):
        cur = self.con.cursor()
        (jid,name) = cur.execute('select jid,name from jobs limit 1').fetchone()
        self.qdel(str(jid))
        return name

    #def last(self):
    #    cur = self.con.cursor()
    #    return cur.lastrowid

    def qdel(self,jid):
        print "jid is:",jid
        cur = self.con.cursor()
        cur.execute('delete from jobs where jid = ?', (jid))
        self.con.commit()
        return 1

    def qstat(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def __allocate(self):
        pass
    
    def __terminate(self):
        pass

if __name__ == "__main__":
    sched = scheduler()
    sched.qsub('test')
    print 'top row id:', sched.qpop()

# let the ball roll
#if __name__ == "__main__":
#    hw_thread = threading.Thread(target = assignTask)
#    hw_thread.daemon = True
#    hw_thread.start()
#    try:
#        time.sleep(500000)
#
#    except KeyboardInterrupt:
#        print '\nGoodbye!'
