import unittest
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
from src import model2, scheduler_mp

class TestScheduler(unittest.TestCase):

    def setUp(self):
        sched = scheduler_mp.scheduler()

    def tearDown(self):
        pass

    def test_del_job(self):
        jid = 649
        db = model2.dal()
        del db.jobs[jid]
        db.commit()

    def test_add_job(self):
        pass

if __name__ == '__main__':
    unittest.main()
