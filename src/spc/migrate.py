from __future__ import absolute_import
from .gluino import DAL, Field
from . import config

class dal(object):
    def __init__(self, uri=config.uri, migrate=False):

        self.db = DAL(uri, migrate=migrate, folder=config.dbdir)

        # must define these here because need to use the db instance
        self.groups =  self.db.define_table('groups', Field('id', 'integer'),
                                         Field('name', 'string'))

        self.users = self.db.define_table('users', Field('id', 'integer'),
                                         Field('user', 'string'),
                                         Field('passwd', 'string'),
                                         Field('email', 'string'),
                                         Field('new_shared_jobs', 'integer'),
                                         Field('priority', 'integer'),
                                         Field('gid', self.db.groups, ondelete="SET NULL"))

        self.user_meta = self.db.define_table('user_meta', Field('id', 'integer'),
                                         Field('uid', self.db.users),
                                         Field('new_shared_jobs', 'integer'),
                                         Field('theme', 'string'))

        self.apps = self.db.define_table('apps', Field('id', 'integer'),
                                       Field('name', 'string'),
                                       Field('description', 'string'),
                                       Field('category', 'string'),
                                       Field('language', 'string'),
                                       Field('input_format', 'string'),
                                       Field('command', 'string'),
                                       Field('assets', 'string'),
                                       Field('preprocess', 'string'),
                                       Field('postprocess', 'string'))

        self.app_user = self.db.define_table('app_user', Field('id', 'integer'),
                                       Field('appid', 'integer'),
                                       Field('uid', 'integer'))

        self.jobs = self.db.define_table('jobs', Field('id', 'integer'),
                                       Field('uid', self.db.users),
                                       Field('app', 'string'),
                                       Field('cid', 'string'),
                                       Field('gid', self.db.groups),
                                       Field('command', 'string'),
                                       Field('state', 'string'),
                                       Field('time_submit', 'string'),
                                       Field('walltime', 'string'),
                                       Field('description', 'string'),
                                       Field('np', 'integer'),
                                       Field('priority', 'integer'),
                                       Field('starred', 'string'),
                                       Field('shared', 'string'))

        self.plots = self.db.define_table('plots', Field('id', 'integer'),
                                         # need to turn on unique in the future, but will cause migration probs for old DBs
                                         # this is needed for running "spc update" b/c primary keys are not specified in spc.json
                                         Field('appid', self.db.apps), # unique=True),
                                         Field('ptype', 'string'),
                                         Field('title', 'string'),
                                         Field('options', 'string'))

        self.datasource = self.db.define_table('datasource', Field('id', 'integer'),
                                                   Field('label', 'string'), # unique=True),
                                                   Field('pltid', self.db.plots),
                                                   Field('filename', 'string'),
                                                   Field('cols', 'string'),
                                                   Field('line_range', 'string'),
                                                   Field('data_def', 'string'))

        self.aws_creds = self.db.define_table('aws_creds', Field('id', 'integer'),
                                                 Field('key', 'string'),
                                                 Field('secret', 'string'),
                                                 Field('account_id', 'string'),
                                                 Field('uid', self.db.users))

        self.aws_instances = self.db.define_table('aws_instances',
                                                        Field('id', 'integer'),
                                                        Field('region', 'string'),
                                                        Field('instance', 'string'),
                                                        Field('itype', 'string'),
                                                        Field('rate', 'double'),
                                                        Field('uid', self.db.users))

        self.disciplines = self.db.define_table('disciplines', Field('name'))

    def commit(self):
        return self.db.commit()
