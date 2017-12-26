#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import threading, time, os, subprocess, signal, datetime
from multiprocessing import Process, BoundedSemaphore, Lock, Manager

from gluino import DAL
from .user_data import user_dir
from . import config

STATE_RUN = 'R'
STATE_QUEUED = 'Q'
STATE_COMPLETED = 'C'
STATE_STOPPED = 'X'

class Scheduler(object):
    """multi-process scheduler"""

    def __init__(self):
        # if any jobs marked in run state when scheduler starts
        # replace their state with X to mark that they have been shutdown
        # db = DAL('sqlite://spc.db'.encode('utf-8').strip(), auto_import=True, migrate=False,
        #          folder='db'.encode('utf-8').strip())
        db = DAL(uri=config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        myset = db(db.jobs.state == STATE_RUN)
        myset.update(state=STATE_STOPPED)
        db.commit()
        self.sem = BoundedSemaphore(config.np)
        self.mutex = Lock()
        # set time zone
        try:
            os.environ['TZ'] = config.time_zone
            time.tzset()
        except: pass

    def poll(self):
        """start polling thread which checks queue status every second"""
        t = threading.Thread(target = self.assignTask)
        t.daemon = True
        t.start()

    def assignTask(self):
        global myjobs
        manager = Manager()
        myjobs = manager.dict()
        while(True):
            self.stop_expired_jobs()
            j = self.qfront()
            if j is not None and j > 0:
                self.start(j)
            time.sleep(1)

    def qsub(self, app, cid, uid, cmd, np, pry, walltime, desc=""):
        """queue job ... really just set state to 'Q'."""
        db = DAL(config.uri, auto_import=True, migrate=False,
                 folder=config.dbdir)
        jid = db.jobs.insert(uid=uid, app=app, cid=cid, command=cmd, state=STATE_QUEUED,
                              description=desc, time_submit=time.asctime(),
                              walltime=walltime, np=np, priority=pry)
        db.commit()
        db.close()
        return str(jid)

    def qfront(self):
        """pop the top job off of the queue that is in a queued 'Q' state"""
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        myorder = db.jobs.priority
        #myorder = db.jobs.priority | db.jobs.id
        row = db(db.jobs.state==STATE_QUEUED).select(orderby=myorder).first()
        db.close()
        if row: return row.id
        else: return None

    def qdel(self,jid):
        """delete job jid from the queue"""
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
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
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        uid = db.jobs(jid).uid
        user = db.users(uid).user
        app = db.jobs(jid).app
        cid = db.jobs(jid).cid
        np = db.jobs(jid).np
        if np > 1: # use mpi
            command = db.jobs(jid).command
            command = config.mpirun + " -np " + str(np) + " " + command
        else: # dont use mpi
            command = db.jobs(jid).command

        # redirect output to appname.out file
        outfn = app + ".out"
        cmd = command + ' > ' + outfn + ' 2>&1 '
        print("cmd:", cmd)

        run_dir = os.path.join(user_dir, user, app, cid)

        # if number procs available fork new process with command
        for i in range(np):
            self.sem.acquire()
        p = Process(target=self.start_job, args=(run_dir,cmd,app,jid,np,myjobs))
        p.start()
        for i in range(np):
            self.sem.release()

    def start_job(self,run_dir,cmd,app,jid,np,myjobs):
        """this is what the separate job process runs"""
        for i in range(np): self.sem.acquire()
        # update state to 'R' for run
        self._set_state(jid,STATE_RUN)
        mycwd = os.getcwd()
        os.chdir(run_dir) # change to case directory

        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        myjobs[jid] = pro

        pro.wait() # wait for job to finish
        myjobs.pop(long(jid),None) # remove job from buffer

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
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        db.jobs[jid] = dict(state=state)
        db.commit()
        db.close()
        self.mutex.release()

    def stop_expired_jobs(self):
        """shutdown jobs that exceed their time limit"""
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        rows = db(db.jobs.state==STATE_RUN).select()
        for row in rows:
            if row:
                walltime = int(row.walltime)
                time_submit = time.mktime(datetime.datetime.strptime(
                              row.time_submit, "%a %b %d %H:%M:%S %Y").timetuple())
                now = time.mktime(datetime.datetime.now().timetuple())
                runtime = now - time_submit
                if runtime > walltime:
                    print("INFO: scheduler stopped job", row.id, "REASON: reached timeout")
                    self.stop(row.id)

        db.close()

    def stop(self,jid):
        p = myjobs.pop(long(jid),None)
        if p: os.killpg(os.getpgid(p.pid), signal.SIGTERM)

        # the following doesn't work because it gets overwritten by line 128 above
        # need a way to feedback to start_job method whether job has been stopped or not
        # db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        # myset = db(db.jobs.id == jid)
        # myset.update(state=STATE_STOPPED)
        # db.commit()
        # db.close()

    def test_qfront(self):
        print(self.qfront())
