#!/usr/bin/env python
import sqlite3 as lite
import time

# Connect to DB 
con = None
try: 
    con = lite.connect('scipaas.db')    

except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

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
        pass

    def qsub(self,path):
        cur = con.cursor()
        print "im here"
        cur.execute('insert into jobs values (null, ?,\'Q\', ?, null, null);',                    (path,time.time()))
        con.commit()

    def qdel(self):
        pass

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

sched = scheduler()
sched.qsub('test')
