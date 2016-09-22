import unittest
import logging
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
from src import model2, scheduler_mp, config

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.dal = model2.dal(uri=config.uri, migrate=True)
        self.sched = scheduler_mp.Scheduler()

    def tearDown(self):
        pass

    def test_qsub(self):
        app = "mendel"
        cid = "TEST00"
        uid = 1
        np = 1
        priority = 2
        desc = "test qsub"

        jid = self.sched.qsub(app, cid, uid, np, priority, desc)

        self.assertTrue(jid > 0)
        # test that the job was written to the db

    def test_qdel(self):
        app = "mendel"
        cid = "TESTXX"
        uid = 1
        np = 1
        priority = 1
        desc = "test qdel"
        jid = self.sched.qsub(app, cid, uid, np, priority, desc)
        self.sched.qdel(jid)
        xjid = self.dal.db.jobs(jid)
        # log= logging.getLogger( "TestScheduler.test_qdel" )
        # log.debug( "jid= %d", int(xjid) )
        self.assertIsNone(xjid)

    # def test_poll(self): pass
    # def test_assignTask(self): pass
    # def test_qfront(self): pass
    # def test_qdel(self): pass
    # def test_qstat(self): pass
    # def test_start(self): pass
    # def test_start_job(self): pass
    # def test_set_state(self): pass
    # def test_stop(self): pass

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "TestScheduler.test_qdel" ).setLevel( logging.DEBUG )
    unittest.main()
