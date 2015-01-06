from dal import DAL, Field

#import macaron
#class Plots(macaron.Model): pass
#class Users(macaron.Model): pass
#class Apps(macaron.Model): pass
#class Wall(macaron.Model): pass

class models(object):
    def __init__(self):
        db = DAL('sqlite://storage.sqlite', auto_import=True, migrate=False)

        self.users = db.define_table('users', Field('id','integer'),
                                          Field('user', 'string'),
                                          Field('passwd','string'))
        self.apps = db.define_table('apps', Field('id','integer'),
                                        Field('name','string'),
                                        Field('description','string'),
                                        Field('category','string'),
                                        Field('language','string'),
                                        Field('input_format','string'))
        self.jobs = db.define_table('jobs', Field('id','integer'),
                                        Field('user','string'),
                                        Field('app','string'),
                                        Field('cid','string'),
                                        Field('state','string'),
                                        Field('time_submit','string'),
                                        Field('description','string'))
        self.plots = db.define_table('plots', Field('id','integer'),
                                          Field('appid','integer'),
                                          Field('type','string'),
                                          Field('filename','string'),
                                          Field('col1','integer'),
                                          Field('col2','integer'),
                                          Field('title','string'))
        self.wall = db.define_table('wall', Field('id','integer'),
                                        Field('jid','integer'),
                                        Field('comment','string'))
