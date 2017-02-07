#!/usr/bin/python
# based on https://github.com/iurisilvio/bottle-chat
import uuid
import inspect

from gevent import monkey; monkey.patch_all()
from gevent.event import Event
from beaker.middleware import SessionMiddleware
import bottle
from bottle import route, request, static_file, template, redirect
import argparse as ap
import config

from model import *

cache_size = 200
cache = []
new_message_event = Event()

app = bottle.app()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': config.user_dir,
    'session.auto': True
}

chatMod = SessionMiddleware(app, session_opts)

root = 0

def bind(app):
    global root
    root = ap.Namespace(**app)

@app.route('/chat')
def main():
    global cache, root
    user = root.authorized()
    session = request.environ.get('beaker.session')
    if cache: session['cursor'] = cache[-1] #['id']
    # clear number of unread messages for current user
    users(user=user).update_record(unread_messages=0)
    db.commit()
    params = {'user': user, 'app': root.active_app()}
    return template('chat', params, messages=cache)

@app.route('/chat/get_messages')
def get_messages():
    global cache
    user = root.authorized()
    return cache

@app.route('/chat/unread_messages')
def get_unread_messages():
    user = root.authorized()
    return str(users(user=user).unread_messages)

@route('/chat/message/new', method='POST', template='chat')
def message_new():
    user = root.authorized()
    global cache, cache_size, new_message_event
    # name = request.environ.get('REMOTE_ADDR') or 'Anonymous'
    name = user
    forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for and name == '127.0.0.1':
        name = forwarded_for
    msg = create_message(name, request.POST.get('body'))
    cache.append(msg)
    if len(cache) > cache_size:
        cache = cache[-cache_size:]
    new_message_event.set()
    new_message_event.clear()

    # increase count in database for every user
    for u in db().select(users.ALL):
        nmsg = users(user=u.user).unread_messages or 0
        users(user=u.user).update_record(unread_messages=nmsg+1)
    db.commit()

    redirect("/chat")

@route('/static/:filename', name='static')
def static_files(filename):
    return static_file(filename, root='./static/')

def create_message(from_, body):
    data = {'id': str(uuid.uuid4()), 'from': from_, 'body': body}
    data['html'] = template('message', message=data)
    return data

if __name__ == '__main__':
    # on server restart clear number of unread messages since the
    # messages will be lost
    users(user.ALL).update_record(unread_messages=0)
    db.commit()
    bottle.run(app=app, server='gevent')
