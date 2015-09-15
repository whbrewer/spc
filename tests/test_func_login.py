import unittest, misc
from bottle import response
import httplib
import sys, os
import sqlite3 as lite
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

user = "xyz123"
passwd = "abcd1234"

class TestLogin(unittest.TestCase):

    def test_login_valid(self):
        url = misc.URL+'/login'
        values = { 'user': 'guest', 'passwd': 'guest' }
        response = misc.post(url,values)
        (code,html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertNotIn("failed",html)

    def test_login_invalid(self):
        url = misc.URL+'/login'
        values = { 'askjdfas': 'guest', 'passwd': 'guest' }
        response = misc.post(url,values)
        (code,html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("failed",html)

class TestRegistration(unittest.TestCase):

    def setUp(self):
        # Connect to DB 
        self.con = None
        try:
            self.con = lite.connect("../db/spc.db")
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def tearDown(self):
        cur = self.con.cursor()
        cur.execute('delete from users where user = (?)',(user,))
        self.con.commit()

    # test valid name 
    def test_registration_valid(self):
        url = misc.URL+'/register'
        values = { 'user': user, 'password1': passwd,
                   'password2': passwd, 'email': 'test@spc.com' }
        (code, html) = misc.post(url,values)
        #print html
        self.assertEqual(code,httplib.OK)
        self.assertNotIn("failed",html)

    # check_user is the function that an Ajax call is send to
    # to check if a user already exists in the DB or not.
    def test_check_user_true(self):
        url = misc.URL+'/check_user'
        values = { 'user': 'guest' }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("true",html)

    def test_check_user_false(self):
        url = misc.URL+'/check_user'
        values = { 'user': 'ak3487234987sdfdfkjl0934823jasldfuiouwaekjflkj' }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("false",html)

if __name__ == '__main__':
    unittest.main()
