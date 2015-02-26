import urllib, urllib2, httplib

URL = 'http://localhost:8081'

def post(url,values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return (response.getcode(), response.read())

#def get(url,values):
