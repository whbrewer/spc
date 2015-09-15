import unittest, misc
from bottle import response
import httplib
import sys, os
import sqlite3 as lite
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
#from spc import config

class TestPlots(unittest.TestCase):

    def setUp(self):
        # Connect to DB 
        self.con = None
        try:
            self.con = lite.connect("../db/spc.db")
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def tearDown(self):
        pass
        #cur = self.con.cursor()
        #cur.execute('delete from users where user = (?)',(user,))
        #self.con.commit()

    # plot functions
        # create a plot
        # delete a plot
        # show a plot
            # bar chart
            # line chart
            # matplot lib route

    # routes:
    #@post('/plots/create')
    #@get('/plots/delete/<pltid>')
    #@get('/plots/edit')
    #@get('/plots/datasource/<pltid>')
    #@post('/plots/datasource_add')
    #@post('/plots/datasource_delete')
    #@get('/plot/<pltid>')

    #def test_delete_plot(self): pass
    #def test_create_plot_flot(self): pass
    #def test_create_plot_matplotlib(self): pass

if __name__ == '__main__':
    unittest.main()
