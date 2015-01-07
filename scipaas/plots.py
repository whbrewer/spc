#import json 
import re, string
import config

class plot(object):

    def __init__(self):
        pass

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
            if re.search(r'#',line): continue
            x = line.split()
            if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                y += '[ ' + str(i) + ', ' + x[col1-1] + '], ' 
                i += 1
        s = "[ %s ]" % y
        return s
