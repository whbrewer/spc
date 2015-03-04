import unittest
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
from scipaas import scheduler_smp

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.sched = scheduler_smp.scheduler()

    def tearDown(self):
        pass

    def test_qsub(self):
        app = "mendel"
        cid = "TEST00"
        user = "guest"
        np = 1
        jid = self.sched.qsub(app,cid,user,np)
        self.assertTrue(jid > 0)
        # test that the job was written to the db

    def test_qdel(self): pass
    def test_poll(self): pass
    def test_assignTask(self): pass
    def test_qfront(self): pass
    def test_qdel(self): pass
    def test_qstat(self): pass
    def test_start(self): pass
    def test_start_job(self): pass
    def test_set_state(self): pass
    def test_stop(self): pass

if __name__ == '__main__':
    unittest.main()
