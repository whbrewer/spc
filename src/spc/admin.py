from __future__ import print_function
from __future__ import absolute_import
import os, shutil, argparse as ap
from .user_data import user_dir
from .model import db, users

from flask import Flask, Blueprint

admin = Blueprint('routes', __name__)

@admin.route('/admin/show_users')
def admin_show_users():
    user = root.authorized()
    if not user == "admin":
        return template("error", err="must be admin to delete")
    result = db().select(users.ALL)
    params = { 'user': user, 'app': root.active_app() }
    return template('admin/users', params, rows=result)

@admin.route('/admin/delete_user', methods=['POST'])
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
