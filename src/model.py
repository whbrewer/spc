from gluino import DAL, Field
import config

#db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
db = DAL(config.uri, migrate=False, folder=config.dbdir)

users = db.define_table('users', Field('id','integer'),
                                 Field('user', 'string'),
                                 Field('passwd','string'),
                                 Field('email','string'),
                                 Field('priority','integer'))
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
                               Field('postprocess','string'),
                               Field('uid','integer'))
# this is also defined in scheduler.py
# need to fix in the future
jobs = db.define_table('jobs', Field('id','integer'),
                               Field('user','string'),
                               Field('app','string'),
                               Field('cid','string'),
                               Field('state','string'),
                               Field('time_submit','string'),
                               Field('description','string'),
                               Field('np','integer'),
                               Field('priority','integer'),
                               Field('starred', 'string'),
                               Field('shared','string'))

plots = db.define_table('plots', Field('id','integer'),
                                 Field('appid',db.apps),
                                 Field('ptype','string'),
                                 Field('title','string'),
                                 Field('options','string'))

datasource = db.define_table('datasource', Field('id','integer'),
                                           Field('pltid','integer'),
                                           Field('filename','string'),
                                           Field('cols','string'),
                                           Field('line_range','string'),
                                           Field('data_def','string'))

aws_creds = db.define_table('aws_creds', Field('id','integer'),
                                         Field('key','string'),
                                         Field('secret','string'),
                                         Field('account_id','string'),
                                         Field('uid','integer'))

aws_instances = db.define_table('aws_instances', Field('id','integer'),
                                                 Field('region','string'),
                                                 Field('instance','string'),
                                                 Field('itype','string'),
                                                 Field('rate','double'),
                                                 Field('uid','integer'))


containers = db.define_table('containers', Field('id','integer'),
                                           Field('containerid','string'),
                                           Field('image','string'),
                                           Field('command','string'),
                                           Field('uid','integer'))
