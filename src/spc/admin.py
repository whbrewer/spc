from bottle import Bottle, jinja2_template as template, redirect, request
import argparse as ap
import os
import shutil

from .model import db, users
from .user_data import user_dir

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.get('/admin/show_users')
def admin_show_users():
    user = root.authorized()
    if not user == "admin":
        return template("error", err="must be admin to delete")
    result = db().select(users.ALL)
    params = { 'user': user, 'app': root.active_app() }
    return template('admin/users', params, rows=result)

@routes.post('/admin/delete_user')
def admin_delete_user():
    user = root.authorized()
    if not user == "admin":
        return template("error", err="must be admin to delete")
    uid = request.forms.uid

    if int(uid) == 0:
        return template("error", err="can't delete admin user")

    if request.forms.del_files == "True":
        path = os.path.join(user_dir, users(uid).user)
        print("deleting files in path:", path)
        if os.path.isdir(path): shutil.rmtree(path)

    del db.users[uid]
    db.commit()

    redirect("/admin/show_users")
