#!/usr/bin/env python
import threading, time, os
import config
from gluon import DAL, Field

#inspired from:
#http://taher-zadeh.com/a-simple-and-dirty-batch-job-scheduler-daemon-in-python/

db = DAL(config.uri, auto_import=True, migrate=False)

apps = db.define_table('apps', Field('id','integer'),
                               Field('name','string'),
                               Field('description','string'),
                               Field('category','string'),
                               Field('language','string'),
                               Field('input_format','string'),
                               Field('command','string'))
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
            time.sleep(1) 

    def qsub(self,app,cid,user):
        state = 'Q'
        jobs.insert(user=user,app=app,cid=cid,state=state,time_submit=time.asctime())
        db.commit()

    def qfront(self):
        # this is giving a recursive cursor error, but it still works
        # it is explained here... fix is to create a thread lock
        # http://stackoverflow.com/questions/26629080/python-and-sqlite3-programmingerror-recursive-use-of-cursors-not-allowed
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
        db.jobs[jid] = dict(state='R')
        db.commit()

        user = db.jobs(jid).user
        app = db.jobs(jid).app
        cid = db.jobs(jid).cid
        command = db(apps.name==app).select()[0]['command']

        #rel_path=(os.pardir+os.sep)*4
        exe = config.apps_dir + os.sep + app + os.sep + app 
        outfn = app + ".out"
        cmd = command + ' >& ' + outfn

        run_dir = config.user_dir + os.sep + user + os.sep + app + os.sep + cid
        thread = threading.Thread(target = self.start_job(run_dir,cmd))
        #thread.daemon = True # run in background
        thread.start()

        # let user know job has ended
        f = open(run_dir+os.sep+outfn,"a")
        f.write("FINISHED EXECUTION")
        f.close()

        db.jobs[jid] = dict(state='C')
        db.commit()

    def start_job(self,run_dir,cmd):
        print 'starting thread to run job:',run_dir, cmd
        os.system("cd " + run_dir + ";" + cmd )

    def stop(self,app):
        os.system("killall " + app)
