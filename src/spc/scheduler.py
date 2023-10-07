from __future__ import print_function
from __future__ import absolute_import
import threading, time, os, subprocess, signal, datetime
from multiprocessing import Process, BoundedSemaphore, Lock, Manager
from peewee import *

from .model import Users, Jobs, Groups, Apps  # Importing the required models
from .user_data import user_dir
from . import config

STATE_RUN = 'R'
STATE_QUEUED = 'Q'
STATE_COMPLETED = 'C'
STATE_STOPPED = 'X'

db = SqliteDatabase(config.dbdir)  # Assuming SQLite, change if using another DB

class Scheduler(object):
    """multi-process scheduler"""

    def __init__(self):
        # Update jobs in run state to stopped state
        query = Jobs.update(state=STATE_STOPPED).where(Jobs.state == STATE_RUN)
        query.execute()
        
        self.sem = BoundedSemaphore(config.np)
        self.mutex = Lock()
        
        # set time zone
        try:
            os.environ['TZ'] = config.time_zone
            time.tzset()
        except: pass

    def poll(self):
        """start polling thread which checks queue status every second"""
        t = threading.Thread(target=self.assignTask)
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
        job = Jobs.create(
            uid=uid,
            app=app,
            cid=cid,
            command=cmd,
            state=STATE_QUEUED,
            description=desc,
            time_submit=time.asctime(),
            walltime=walltime,
            np=np,
            priority=pry
        )
        return str(job.id)

    def qfront(self):
        job = Jobs.select().where(Jobs.state == STATE_QUEUED).order_by(Jobs.priority.asc()).first()
        return job.id if job else None

    def qdel(self, jid):
        query = Jobs.delete().where(Jobs.id == jid)
        query.execute()

    def qstat(self):
        return Jobs.select().where(Jobs.state == STATE_QUEUED).count()

    def start(self, jid):
        job = Jobs.get(Jobs.id == jid)
        user = Users.get(Users.id == job.uid)
        app = job.app
        cid = job.cid
        np = job.np
        command = job.command if np <= 1 else config.mpirun + " -np " + str(np) + " " + command

        outfn = app + ".out"
        cmd = command + ' > ' + outfn + ' 2>&1 '
        print("cmd:", cmd)

        run_dir = os.path.join(user_dir, user.user, app, cid)
        for i in range(np):
            self.sem.acquire()
        p = Process(target=self.start_job, args=(run_dir, cmd, app, jid, np, myjobs))
        p.start()
        for i in range(np):
            self.sem.release()

    def start_job(self, run_dir, cmd, app, jid, np, myjobs):
        for i in range(np): self.sem.acquire()
        self._set_state(jid, STATE_RUN)
        mycwd = os.getcwd()
        os.chdir(run_dir)  # change to case directory

        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        myjobs[jid] = pro

        pro.wait()  # wait for job to finish
        myjobs.pop(long(jid), None)  # remove job from buffer

        outfn = app + ".out"
        with open(outfn, "a") as f:
            f.write("FINISHED EXECUTION")

        os.chdir(mycwd)
        self._set_state(jid, STATE_COMPLETED)
        for i in range(np):
            self.sem.release()

    def _set_state(self, jid, state):
        with db.atomic():
            job = Jobs.get(Jobs.id == jid)
            job.state = state
            job.save()

    def stop_expired_jobs(self):
        for job in Jobs.select().where(Jobs.state == STATE_RUN):
            walltime = int(job.walltime)
            time_submit = time.mktime(datetime.datetime.strptime(
                job.time_submit, "%a %b %d %H:%M:%S %Y").timetuple())
            now = time.mktime(datetime.datetime.now().timetuple())
            runtime = now - time_submit
            if runtime > walltime:
                print("INFO: scheduler stopped job", job.id, "REASON: reached timeout")
                self.stop(job.id)

    def stop(self, jid):
        p = myjobs.pop(long(jid), None)
        if p: os.killpg(os.getpgid(p.pid), signal.SIGTERM)

    def test_qfront(self):
        print(self.qfront())

