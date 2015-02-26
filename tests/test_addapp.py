import unittest, misc
from bottle import response
import urllib, urllib2, httplib
import sqlite3 as lite
import sys, os, shutil
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

#@get('/addapp')
#@post('/addapp/<step>')

# test adding app as one user and deleting as another user
# test checkbox
# test hidden
# test textbox
# test select

# it is important that the name of this app is not an app that
# already is installed in the system
APP = "xyz123"

class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Connect to DB 
        self.con = None
        try:
            self.con = lite.connect("db/scipaas.db")
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def tearDown(self):
        # remove the test app from the database
        cur = self.con.cursor()
        cur.execute('delete from apps where name = (?)',(APP,))
        self.con.commit()
        # remove directory created in apps folder
        path = os.path.join("apps", APP)
        if os.path.isdir(path):
            shutil.rmtree(path)
        # remove template file that was created
        try: os.remove('views/apps/'+APP+'.tpl')
        except OSError: pass

    #@unittest.skip("skipping test...")
    # test app name that does not exist
    def test_step0_noexist(self):
        appname = 'dna'
        url = misc.URL+'/app_exists/'+appname
        values = { 'appname': appname }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("true",html)

    #@unittest.skip("skipping test...")
    # test app name that does not exist
    def test_step0_exists(self):
        appname = APP
        url = misc.URL+'/app_exists/' + appname
        values = { 'appname': appname } 
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertNotIn("true",html)
    
    def test_addapp(self):
        """test /addapp route"""
        url = misc.URL+'/addapp'
        response = urllib2.urlopen(url)
        html = response.read()
        self.assertEqual(response.getcode(),httplib.OK)
        self.assertIn("Enter name of app",html)

    def test_step0(self):
        """enter app name"""
        url = misc.URL+'/addapp/step1'
        appname = APP
        values = { 'appname': appname } 
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("configure app",html)

    def test_step1(self):
        """enter config options about app"""
        url = misc.URL+'/addapp/step2'
        appname = APP
        description = 'this is a test case'
        category = 'bioinformatics'
        command = '../../../../apps/'+appname+os.sep+appname
        user = 'tester'
        values = { 'appname': appname, 'description': description,
                   'category': category, 'command': command, 'user': user } 
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("Upload zip file",html)

    def test_step2(self):
        """upload zip file"""
        import multipart
        # Create the form with simple fields
        form = multipart.MultiPartForm()
        form.add_field('appname', APP)
        form.add_field('input_format', 'ini')
        f = open(APP+'.zip',"r")
        form.add_file('upload', APP+'.zip', fileHandle=f)
        # Build the request
        request = urllib2.Request(misc.URL+'/addapp/step3')
        body = str(form)
        request.add_header('Content-type', form.get_content_type())
        request.add_header('Content-length', len(body))
        request.add_data(body)
        #print request.get_data()
        # server response
        html = urllib2.urlopen(request).read()
        self.assertNotIn("no file selected", html)
        
    def test_step3(self):
        url = misc.URL+'/addapp/step4'
        appname = APP
        input_format = 'ini'
        # contents not used just for user to see
        # so just pass dummy string in
        values = { 'input_format': input_format, 'appname': appname,
                   'contents': 'blah' }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("assign html input types",html)

    def test_step4(self):
        url = misc.URL+'/addapp/step5'
        bool_rep = 'T'
        appname = APP
        input_format = 'ini'
        html_tags = ['text', 'hidden', 'select', 'checkbox']
        descriptions = ['this is a textbox', 'this is a hidden input', 
                        'this is a select tag', 'this is a checkbox']
        keys = ['par1','par2','par3']
        values = {'bool_rep': bool_rep, 'input_format': input_format, 
                  'appname': appname , 'descriptions': descriptions, 
                  'html_tags': html_tags, 'keys': keys }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("Template file successfully written",html)

if __name__ == '__main__':
    unittest.main()

