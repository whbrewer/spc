#!/usr/bin/python

def preprocess(params,fn):
    str = ''
    if fn == 'fpg.in':  
        """convert input key/value params to command-line style args"""
        for key, value in (params.iteritems()):
            if key == 't_pseudo_data':
               if value=='true': value = ''
               else: continue # don't output anything when this param is false
            option = '-' + key.split('_')[0] # extract first letter
            str += option + value + ' ' 
        return str
    else:
        for key, value in (params.iteritems()):
            str += key + ' ' + value + '\n'
        return str

def postprocess(path,line1,line2):
    """return data as an array...
    turn data that looks like this:
        100       0.98299944  200       1.00444448      300       0.95629907      
    into something that looks like this:
        [[100, 0.98299944], [200, 1.00444448], [300, 0.95629907], ... ]"""
    y = []
    data = open(path, 'rU').readlines()
    subdata = data[line1:line2]
    xx = []; yy = []
    for d in subdata: 
        xy = d.split()
        for (j,x) in enumerate(xy):
            if j%2: yy += [x]
            else:   xx += [x]
    data = [] 
    z = zip(xx,yy)
    for (x,y) in z:
        a = [ int(x), float(y) ]
        data += [ a ]
    return data
