from peewee import Model, CharField, IntegerField, ForeignKeyField, DoubleField, SqliteDatabase
from . import config

# Set up the Peewee database
db = SqliteDatabase(config.uri)  # Assuming config.dbdir points to a SQLite database file

class BaseModel(Model):
    class Meta:
        database = db

class Groups(BaseModel):
    name = CharField()

class Users(BaseModel):
    user = CharField()
    passwd = CharField()
    email = CharField()
    new_shared_jobs = IntegerField()
    priority = IntegerField()
    gid = ForeignKeyField(Groups, backref='users', null=True)

class UserMeta(BaseModel):
    uid = ForeignKeyField(Users, backref='user_meta')
    new_shared_jobs = IntegerField()
    theme = CharField()

class Apps(BaseModel):
    name = CharField()
    description = CharField()
    category = CharField()
    language = CharField()
    input_format = CharField()
    command = CharField()
    assets = CharField()
    preprocess = CharField()
    postprocess = CharField()

class AppUser(BaseModel):
    appid = IntegerField()
    uid = IntegerField()

class Jobs(BaseModel):
    uid = ForeignKeyField(Users, backref='jobs')
    app = CharField()
    cid = CharField()
    gid = ForeignKeyField(Groups, backref='jobs', null=True)
    command = CharField()
    state = CharField()
    time_submit = CharField()
    walltime = CharField()
    description = CharField()
    np = IntegerField()
    priority = IntegerField()
    starred = CharField()
    shared = CharField()

class Plots(BaseModel):
    appid = ForeignKeyField(Apps, backref='plots')
    ptype = CharField()
    title = CharField()
    options = CharField()

class DataSource(BaseModel):
    label = CharField()
    pltid = ForeignKeyField(Plots, backref='data_sources')
    filename = CharField()
    cols = CharField()
    line_range = CharField()
    data_def = CharField()

class AWSCreds(BaseModel):
    key = CharField()
    secret = CharField()
    account_id = CharField()
    uid = ForeignKeyField(Users, backref='aws_creds')

class AWSInstances(BaseModel):
    region = CharField()
    instance = CharField()
    itype = CharField()
    rate = DoubleField()
    uid = ForeignKeyField(Users, backref='aws_instances')

