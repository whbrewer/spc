from dal import DAL, Field
import config

db = DAL(config.uri, auto_import=True, migrate=False)

users = db.define_table('users', Field('id','integer'),
                                 Field('user', 'string'),
                                 Field('passwd','string'))
apps = db.define_table('apps', Field('id','integer'),
                               Field('name','string'),
                               Field('description','string'),
                               Field('category','string'),
                               Field('language','string'),
                               Field('input_format','string'))
jobs = db.define_table('jobs', Field('id','integer'),
                               Field('user','string'),
                               Field('app','string'),
                               Field('cid','string'),
                               Field('state','string'),
                               Field('time_submit','string'),
                               Field('description','string'))
plots = db.define_table('plots', Field('id','integer'),
                                 Field('appid',db.apps),
                                 Field('ptype','string'),
                                 Field('filename','string'),
                                 Field('cols','string'),
                                 Field('line_range','string'),
                                 Field('title','string'),
                                 Field('options','string'))
wall = db.define_table('wall', Field('id','integer'),
                               Field('jid',db.jobs),
                               Field('comment','string'))
