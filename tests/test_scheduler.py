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
        cid = "cbb0af"
        user = "wes"
        np = 1
        jid = self.sched.qsub(app,cid,user,np)
        self.assertTrue(jid > 0)

# qfront test

# qdel test
#print 'rowid:', sched.qpop()


#assertEqual(a, b)   a == b   
#assertNotEqual(a, b)    a != b   
#assertTrue(x)   bool(x) is True  
#assertFalse(x)  bool(x) is False     
#assertIs(a, b)  a is b  2.7
#assertIsNot(a, b)   a is not b  2.7
#assertIsNone(x) x is None   2.7
#assertIsNotNone(x)  x is not None   2.7
#assertIn(a, b)  a in b  2.7
#assertNotIn(a, b)   a not in b  2.7
#assertIsInstance(a, b)  isinstance(a, b)    2.7
#assertNotIsInstance(a, b)   not isinstance(a, b)    2.7

if __name__ == '__main__':
    unittest.main()
