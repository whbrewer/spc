from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import config

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = config.uri  # Ensure this is correctly set up
#db = SQLAlchemy(app)
db = SQLAlchemy()

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    passwd = db.Column(db.String)
    email = db.Column(db.String)
    new_shared_jobs = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    gid = db.Column(db.Integer)

class UserMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    new_shared_jobs = db.Column(db.Integer)
    theme = db.Column(db.String)

class Apps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    language = db.Column(db.String)
    input_format = db.Column(db.String)
    command = db.Column(db.String)
    assets = db.Column(db.String)
    preprocess = db.Column(db.String)
    postprocess = db.Column(db.String)

class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.Integer)
    uid = db.Column(db.Integer)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    app = db.Column(db.String)
    cid = db.Column(db.String)
    gid = db.Column(db.Integer, db.ForeignKey('groups.id'))
    command = db.Column(db.String)
    state = db.Column(db.String)
    time_submit = db.Column(db.String)
    walltime = db.Column(db.String)
    description = db.Column(db.String)
    np = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    starred = db.Column(db.String)
    shared = db.Column(db.String)

class Plots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.Integer, db.ForeignKey('apps.id'))
    ptype = db.Column(db.String)
    title = db.Column(db.String)
    options = db.Column(db.String)

class DataSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    pltid = db.Column(db.Integer, db.ForeignKey('plots.id'))
    filename = db.Column(db.String)
    cols = db.Column(db.String)
    line_range = db.Column(db.String)
    data_def = db.Column(db.String)

class AWSCreds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    secret = db.Column(db.String)
    account_id = db.Column(db.String)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

class AWSInstances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String)
    instance = db.Column(db.String)
    itype = db.Column(db.String)
    rate = db.Column(db.Float)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

