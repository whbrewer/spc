import unittest
import sys
sys.path.insert(0, '../')

import scipaas
#import bottle
#import bottle.ext.sqlite

class SciPaasTest(unittest.TestCase):
    def test_overview(self):
        print scipaas.overview()



# user login
# user registration

# app functions
# add/create app
# deleting app
# uploading app
    # test that when file unzips the unzipped directory is the same as the zip file name

# inputs
# outputs
# plot functions
# schedule functions

# others:
# if click list when directory doesnt exist >> error 405
# if click Upload but file not first selected >> error
# upload verify works with .in and exe file
# verify throws error with no .in file
# verify throws error with no exe file
# test if writing parameters correctly especially test booleans, integers, strings, etc.
