#!/usr/bin/env python
import threading, time, os
import config
from multiprocessing import Process, BoundedSemaphore, Lock, Manager
import subprocess, signal
from gluino import DAL, Field

STATE_RUN = 'R'
STATE_QUEUED = 'Q'
STATE_COMPLETED = 'C'

class Scheduler(object):
    """multi-process scheduler"""

    def __init__(self):
        # if any jobs marked in run state when scheduler starts
        # replace their state with X to mark that they have been shutdown
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        myset = db(db.jobs.state == 'R')
        myset.update(state='X')
        db.commit()
        self.sem = BoundedSemaphore(config.np)
        self.mutex = Lock()

    def poll(self):
        """start polling thread which checks queue status every second"""
        t = threading.Thread(target = self.assignTask)
        t.start()

    def assignTask(self):
        global dict_jobs
        manager = Manager()
        dict_jobs = manager.dict()
        while(True):
            j = self.qfront()
            if j is not None and j > 0:
                self.start(j)
            time.sleep(1)

    def qsub(self,app,cid,uid,np,pry,desc=""):
        """queue job ... really just set state to 'Q'."""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        jid = db.jobs.insert(uid=uid, app=app, cid=cid, state=STATE_QUEUED,
                              description=desc, time_submit=time.asctime(), np=np, priority=pry)
        db.commit()
        db.close()
        return str(jid)

    def qfront(self):
        """pop the top job off of the queue that is in a queued 'Q' state"""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        myorder = db.jobs.priority
        #myorder = db.jobs.priority | db.jobs.id
        row = db(db.jobs.state==STATE_QUEUED).select(orderby=myorder).first()
        db.close()
        if row: return row.id
        else: return None

    def qdel(self,jid):
        """delete job jid from the queue"""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        del db.jobs[jid]
        db.commit()
        db.close()

    def qstat(self):
        """return the number of jobs in a queued 'Q' state"""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        return db(db.jobs.state==STATE_QUEUED).count()
        db.close()

    def start(self,jid):
        """start running a job by creating a new process"""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        uid = db.jobs(jid).uid
        user = db.users(uid).user
        app = db.jobs(jid).app
        cid = db.jobs(jid).cid
        np = db.jobs(jid).np
        if np > 1: # use mpi
            command = db.apps(name=app).command
            command = config.mpirun + " -np " + str(np) + " " + command
        else: # dont use mpi
            command = db.apps(name=app).command

        exe = os.path.join(config.apps_dir,app,app)
        outfn = app + ".out"
        cmd = command + ' > ' + outfn + ' 2>&1 '

        run_dir = os.path.join(config.user_dir,user,app,cid)

        # if number procs available fork new process with command
        for i in range(np):
            self.sem.acquire()
        p = Process(target=self.start_job, args=(run_dir,cmd,app,jid,np,dict_jobs))
        p.start()
        for i in range(np):
            self.sem.release()

    def start_job(self,run_dir,cmd,app,jid,np,dict_jobs):
        """this is what the separate job process runs"""
        for i in range(np):
            self.sem.acquire()
        # update state to 'R' for run
        self._set_state(jid,STATE_RUN)
        mycwd = os.getcwd()
        os.chdir(run_dir) # change to case directory
        
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        dict_jobs[jid] = pro

        pro.wait() # wait for job to finish

        # let user know job has ended
        outfn = app + ".out"
        with open(outfn,"a") as f:
            f.write("FINISHED EXECUTION")

        # update state to 'C' for completed
        os.chdir(mycwd)
        self._set_state(jid,STATE_COMPLETED)
        for i in range(np):
            self.sem.release()

    def _set_state(self,jid,state):
        """update state of job"""
        self.mutex.acquire()
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        db.jobs[jid] = dict(state=state)
        db.commit()
        db.close()
        self.mutex.release()

    def stop(self,jid):
        p = dict_jobs.pop(long(jid),None)
        if p: os.killpg(os.getpgid(p.pid), signal.SIGTERM)

    def test_qfront(self):
        print self.qfront()
