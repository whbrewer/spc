#import json 
import re, string
import config
import sqlite3 as lite

class plot(object):

    def __init__(self):
        # Connect to DB 
        self.con = None
        try:
            self.con = lite.connect(config.db)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def get_data(self,fn,col1,col2):
        y = ''
        for line in open(fn, 'rU'):
            # don't parse comments
            #print line
            if re.search(r'#',line): continue
            x = line.split()
            if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                y += '[ ' + x[col1-1] + ', ' + x[col2-1] + '], ' 
        s = "[ %s ]" % y
        return s

    def get_ticks(self,fn,col1,col2):
        y = ''
        i = 0
        for line in open(fn, 'rU'):
            # don't parse comments
            #print line
            if re.search(r'#',line): continue
            x = line.split()
            if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                y += '[ ' + str(i) + ', ' + x[col1-1] + '], ' 
                i += 1
        s = "[ %s ]" % y
        return s

    def create(self,appid,ptype,fn,col1,col2,title):
        #insert into plots values (NULL,12,'xyplot','burger.dat',0,1);
        # use try except here...
        print 'creating plot: ',appid,ptype,fn,col1,col2
        cur = self.con.cursor()
        cur.execute('insert into plots values (NULL,?,?,?,?,?,?)',(appid,ptype,fn,col1,col2,title))
        self.con.commit()

#    def read(self,app,pltid):
#        cur = self.con.cursor()
#        # in the future this has to support reading multiple plots
#        result = cur.execute('select type, filename, col1, col2, title from apps natural join plots where name=? and id=?',(app,pltid)).fetchone()
#        if result is None:
#            return None
#        else:
#            return (result[0],result[1],result[2],result[3],result[4])

    def show(self):
        cur = self.con.cursor()
        result = cur.execute('select * from plots')
        #print result

    def delete(self,pid):
        cur = self.con.cursor()
        cur.execute('delete from plots where id = (?)',(pid,))
        self.con.commit()

    def update(self,pid):
        pass

#CREATE TABLE plots(pltid integer primary key autoincrement, appid integer,  type varchar(80), filename varchar(80), col1 integer, col2 integer, foreign key (appid) references apps(appid));
#insert into plots values (1,11,'xyplot','<cid>.000.hst',0,1);
