#!/usr/bin/env python
import threading, time, os
import config
from dal import DAL, Field

#inspired from:
#http://taher-zadeh.com/a-simple-and-dirty-batch-job-scheduler-daemon-in-python/

db = DAL(config.db, auto_import=True, migrate=False)

jobs = db.define_table('jobs', Field('id','integer'),
                               Field('user','string'),
                               Field('app','string'),
                               Field('cid','string'),
                               Field('state','string'),
                               Field('time_submit','string'),
                               Field('description','string'))

class scheduler(object):

    def __init__(self):
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
        state = 'Q'
        jobs.insert(user=user,app=app,cid=cid,state=state,time_submit=time.asctime())
        db.commit()

    def qfront(self):
        jid = db.jobs(db.jobs.state=='Q')
        if jid: return jid.id
        else: return None

    def qdel(self,jid):
        del db.jobs[jid]
        db.commit()
        return 1

    def qstat(self):
        return db(db.jobs.state=='Q').count()

    def start(self,jid):
        global myapps
        db.jobs[jid] = dict(state='R')
        db.commit()

        user = db.jobs(jid).user
        app = db.jobs(jid).app
        cid = db.jobs(jid).cid

        rel_path=(os.pardir+os.sep)*4
        run_dir = config.user_dir + os.sep + user + os.sep + app + os.sep + cid
        exe = config.apps_dir + os.sep + app + os.sep + app
        outfn = app + ".out"
        cmd = rel_path + exe + " " + app + ".ini >& " + outfn
        t = threading.Thread(target = self.start_job(run_dir,cmd))
        t.start()

        db.jobs[jid] = dict(state='C')
        db.commit()

    def start_job(self,run_dir,cmd):
        print 'starting thread to run job:',run_dir, cmd
        os.system("cd " + run_dir + ";" + cmd )

    def stop(self,app):
        os.system("killall " + app)
