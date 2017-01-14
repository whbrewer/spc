#!/usr/bin/env python


# base class for scheduler

class Schedule_base(object):

    def __init__(self): pass
    def poll(self): pass
    def assignTask(self): pass
    def qsub(self, app, cid, uid, np, pry, walltime, desc=""): pass
    def qfront(self): pass
    def qdel(self,jid): pass
    def qstat(self): pass
    def start(self,jid): pass
    def start_job(self,run_dir,cmd,app,jid): pass
    def stop(self,jid): pass
