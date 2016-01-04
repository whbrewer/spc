#!/usr/bin/env python
import threading, time, os
import config
from gluino import DAL, Field
import subprocess, signal

#inspired from:
#http://taher-zadeh.com/a-simple-and-dirty-batch-job-scheduler-daemon-in-python/

db = DAL(config.uri, auto_import=False, migrate=False, folder=config.dbdir)

apps = db.define_table('apps', Field('id','integer'),
                               Field('name','string'),
                               Field('description','string'),
                               Field('category','string'),
                               Field('language','string'),
                               Field('input_format','string'),
                               Field('command','string'))

users = db.define_table('users', Field('id','integer'),
                                 Field('user', 'string'),
                                 Field('passwd','string'),
                                 Field('email','string'),
                                 Field('priority','integer'))

jobs = db.define_table('jobs', Field('id','integer'),
                               Field('uid',db.users),
                               Field('app','string'),
                               Field('cid','string'),
                               Field('state','string'),
                               Field('time_submit','string'),
                               Field('description','string'),
                               Field('np','integer'),
                               Field('priority','integer'),
                               Field('starred', 'string'),
                               Field('shared','string'))

class Scheduler(object):
    """simple single process scheduler"""
    def __init__(self):
        # if any jobs marked in run state when scheduler starts
        # replace their state with X to mark that they have been shutdown
        myset = db(db.jobs.state == 'R')
        myset.update(state='X')
        db.commit()

    def poll(self):
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

    def qsub(self,app,cid,uid,np,pry,desc=""):
        state = 'Q'
        jid = jobs.insert(uid=uid, app=app, cid=cid, state=state, description=desc,
                          time_submit=time.asctime(), np=np, priority=pry)
        db.commit()
        return str(jid)

    def qfront(self):
        # this is giving a recursive cursor error, but it still works
        # it is explained here... fix is to create a thread lock
        # http://stackoverflow.com/questions/26629080/python-and-sqlite3-programmingerror-recursive-use-of-cursors-not-allowed
        row = db.jobs(db.jobs.state=='Q')
        if row: return row.id
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

        uid = jobs(jid).uid
        user = users(uid).user
        app = jobs(jid).app
        cid = jobs(jid).cid
        np = jobs(jid).np
        if np > 1:
            command = apps(name=app).command
            command = config.mpirun + " -np " + str(np) + " " + command
        else: # dont use mpi
            command = apps(name=app).command

        exe = os.path.join(config.apps_dir,app,app)
        outfn = app + ".out"
        cmd = command + ' > ' + outfn + ' 2>&1 '

        run_dir = os.path.join(config.user_dir,user,app,cid)
        thread = threading.Thread(target = self.start_job(run_dir,cmd,app,jid))
        thread.start()

    def start_job(self,run_dir,cmd,app,jid):
        print 'starting thread to run job:',run_dir, cmd
        global popen
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        popen = subprocess.Popen(cmd, cwd=run_dir, stdout=subprocess.PIPE,
                                 shell=True, preexec_fn=os.setsid)
        popen.wait()

        # let user know job has ended
        outfn = app + ".out"
        with open(os.path.join(run_dir,outfn),"a") as f:
            f.write("FINISHED EXECUTION")

        # update state to completed
        db.jobs[jid] = dict(state='C')
        db.commit()

    def stop(self):
        # Send the signal to all the process groups
        try: # if running
            os.killpg(popen.pid, signal.SIGTERM)
        except: # if not running
            return -1




