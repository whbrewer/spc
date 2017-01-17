#!/usr/bin/env python
import threading, time, os
import config
from gluino import DAL, Field
import subprocess, signal

# web socket stuff
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from bottle import request, Bottle, abort
# http://stackoverflow.com/a/4896288/2636544
from Queue import Queue, Empty
app = Bottle()

@app.route('/websocket')
def handle_websocket():
    global wsock
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            #wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break

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
                                 Field('unread_messages','integer'),
                                 Field('new_shared_jobs','integer'),
                                 Field('priority','integer'))

jobs = db.define_table('jobs', Field('id','integer'),
                               Field('uid',db.users),
                               Field('app','string'),
                               Field('cid','string'),
                               Field('state','string'),
                               Field('time_submit','string'),
                               Field('walltime','string'),
                               Field('description','string'),
                               Field('np','integer'),
                               Field('priority','integer'),
                               Field('starred', 'string'),
                               Field('shared','string'))

# http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''
 
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue
 
    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)
 
    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

class Scheduler(object):
    """simple single process scheduler"""
    def __init__(self):
        # if any jobs marked in run state when scheduler starts
        # replace their state with X to mark that they have been shutdown
        myset = db(db.jobs.state == 'R')
        myset.update(state='X')
        db.commit()
        # set time zone
        try:
            os.environ['TZ'] = config.time_zone
            time.tzset()
        except: pass

    def poll(self):
        # start polling thread
        t = threading.Thread(target = self.assignTask)
        t.daemon = True
        t.start()

    def start_data_server(self):
        t = threading.Thread(target = self.start_data_server2)
        t.daemon = True
        t.start()

    def start_data_server2(self):
        print "Starting websocket data server..."
        server = WSGIServer(("0.0.0.0", 8581), app,
                            handler_class=WebSocketHandler)
        server.serve_forever()

    def assignTask(self):
        while(True):
            #print "scheduler:", self.qstat(), "jobs in queued state",
            #time.asctime()
            j = self.qfront()
            if j is not None and j > 0:
                self.start(j)
            time.sleep(1)

    def qsub(self, app, cid, uid, np, pry, walltime, desc=""):
        state = 'Q'
        jid = jobs.insert(uid=uid, app=app, cid=cid, state=state, description=desc,
                          walltime=walltime, time_submit=time.asctime(), np=np, priority=pry)
        db.commit()
        return str(jid)

    def qfront(self):
        # this is giving a recursive cursor error, but it still works
        # it is explained here... fix is to create a thread lock
        # http://stackoverflow.com/questions/26629080
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
        # cmd = command + ' >& ' + outfn
        cmd = command

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
        stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(popen.stdout, stdout_queue)
        stdout_reader.start()

        outfn = app + ".out"
        fout = open(os.path.join(run_dir,outfn),"w")
        lines = []

        # Check the queues if we received some output (until there is nothing more to get).
        while not stdout_reader.eof():
            # Show what we received from standard output.
            while not stdout_queue.empty():
                line = stdout_queue.get()
                fout.write(str(line))
                wsock.send(line)

        popen.wait()
        fout.close()

        # let user know job has ended
        with open(os.path.join(run_dir,outfn),"a") as f:
            f.write("FINISHED EXECUTION")

        # update state to completed
        db.jobs[jid] = dict(state='C')
        db.commit()

    def stop(self,jid):
        # Send the signal to all the process groups
        try: # if running
            os.killpg(popen.pid, signal.SIGTERM)
        except: # if not running
            return -1

