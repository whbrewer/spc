#import json 
import re, string
import config

class plot(object):

    def __init__(self):
        pass

    def get_data(self,fn,col1,col2,line1=1,line2=1e6):
        """return data as string in format [ [x1,y1], [x2,y2], ... ]"""
        y = ''
        lineno = 0
        data = open(fn, 'rU').readlines()
        nlines = len(data)
        # allow for tailing a file by giving a negative range, e.g. -100:10000
        if line1 < 0:
            line1 += nlines
        for line in data:
            lineno += 1
            if lineno >= line1 and lineno <= line2:
                # don't parse comments
                if re.search(r'#',line): continue
                x = line.split()
                #following line doesnt work when NaN's in another column
                #if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                y += '[ ' + x[col1-1] + ', ' + x[col2-1] + '], ' 
        s = "[ %s ]" % y
        return s

    def get_column_of_data(self,fn,col,line1=1,line2=1e6):
        y = []
        lineno = 0
        data = open(fn, 'rU').readlines()
        nlines = len(data)
        # allow for tailing a file by giving a negative range, e.g. -100:10000
        if line1 < 0:
            line1 += nlines
        for line in data:
            lineno += 1
            if lineno >= line1 and lineno <= line2:
                # don't parse comments
                if re.search(r'#',line): continue
                x = line.split()
                #following line doesnt work when NaN's in another column
                #if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                y += [ x[col-1] ] 
        return y

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
