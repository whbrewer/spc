#!/usr/bin/python
from scipaas import apps as appmod

def preprocess(params):
    """convert input key/value params to command-line style args"""
    str = ''
    for key, value in (params.iteritems()):
        option = '-' + key.split('_')[0] # extract first letter
        str += option + params[key] + ' ' 
    return str

def postprocess(path,line1,line2):
    """return data as an array..."""
    y = []
    data = open(path, 'rU').readlines()
    subdata = data[line1:line2]
    #subdata = data[47:59]
    xx = []; yy = []
    for d in subdata: 
        xy = d.split()
        for (j,x) in enumerate(xy):
            if j%2: # generations
                yy += [x]
            else: # fitness
                xx += [x]
    data = [] 
    z = zip(xx,yy)
    for (x,y) in z:
        a = [ int(x), float(y) ]
        data += [ a ]
    return data

