#!/usr/bin/env python
import sqlite3 as lite
import config

class user(object):

    def __init__(self):
        # Connect to DB 
        self.con = None
        try:
            self.con = lite.connect(config.database)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def create(self,user,passwd):
        # use try except here...
        cur = self.con.cursor()
        cur.execute('insert into users values (NULL,?,?)',(user,passwd))
        self.con.commit()

    def delete(self,uid):
        cur = self.con.cursor()
        cur.execute('delete from users where uid = (?)',(uid,))
        self.con.commit()

    def update(self,uid):
        pass
    
    def show(self):
        cur = self.con.cursor()
        result = cur.execute('select * from users')
        #print result
        for i in result: print i

    def authenticate(self,user,passwd):
        cur = self.con.cursor()
        try:
            (dbpasswd,) = cur.execute('select pass from users where user = \'' + user + '\';').fetchone()
            if passwd == dbpasswd: 
                return True
            else: # user correct, but password not correct
                return False
        except:   # user is not in db
            return False

if __name__ == "__main__":
    # tests:
    # can handle right user/pass
    # wrong user right pass
    # right user wrong pass
    u = user()
    print "authentication test:", u.authenticate('wes','john3.16')
    #print "insert test:", u.create('bob','jones')
    #u.delete(2)
    u.show()

