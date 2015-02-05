from dal import DAL, Field
import config

db = DAL(config.uri, auto_import=True, migrate=False)

users = db.define_table('users', Field('id','integer'),
                                 Field('user', 'string'),
                                 Field('passwd','string'))
# this is also defined in scheduler.py
# need to fix in the future
apps = db.define_table('apps', Field('id','integer'),
                               Field('name','string'),
                               Field('description','string'),
                               Field('category','string'),
                               Field('language','string'),
                               Field('input_format','string'),
                               Field('command','string'),
                               Field('preprocess','string'),
                               Field('postprocess','string'))
# this is also defined in scheduler.py
# need to fix in the future
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
                                 Field('title','string'),
                                 Field('options','string'),
                                 Field('datadef','string'))
datasource = db.define_table('datasource', Field('id','integer'),
                                           Field('label','string'),
                                           Field('ptype','string'),
                                           Field('color','string'),
                                           Field('pltid','integer'),
                                           Field('filename','string'),
                                           Field('cols','string'),
                                           Field('line_range','string'))
wall = db.define_table('wall', Field('id','integer'),
                               Field('jid',db.jobs),
                               Field('comment','string'))
aws = db.define_table('aws_credentials', Field('id','integer'),
                                         Field('key','string'),
                                         Field('secret','string'),
                                         Field('account_id','string'))
aws = db.define_table('aws_instances', Field('id','integer'),
                                       Field('region','string'),
                                       Field('instance','string'),
                                       Field('type','string'),
                                       Field('rate','double'))
