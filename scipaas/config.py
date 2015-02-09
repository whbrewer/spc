#!/usr/bin/env python
db = 'scipaas.db'
uri = 'sqlite://'+db
apps_dir = 'apps'
user_dir = 'user_data'
tmp_dir = 'static/tmp'
# server options are: cgi, flup, wsgiref, waitress, cherrypy, paste, fapws3, 
# tornado, gae, twisted, diesel, meinheld, gunicorn, eventlet, gevent, 
# rocket, bjoern, auto
server = 'cherrypy'
#server = 'rocket'
