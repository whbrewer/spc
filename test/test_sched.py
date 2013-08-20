#import unittest
#import sys
#sys.path.insert(0, '../')

import scheduler

sched = scheduler.scheduler()

sched.qsub('test')

print 'rowid:', sched.qpop()

