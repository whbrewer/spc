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
    if cache: session['cursor'] = cache[-1]['id']
    return template('chat', messages=cache)

@route('/a/message/new', method='POST', template='chat')
def message_new():
    user = root.authorized()
    global cache
    global cache_size
    global new_message_event
    name = request.environ.get('REMOTE_ADDR') or 'Anonymous'
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
    #return msg
    redirect("/chat")

@route('/a/message/updates', method='POST', template='chat')
def message_updates(session):
    global cache
    global new_message_event
    cursor = session.get('cursor')
    if not cache or cursor == cache[-1]['id']:
         new_message_event.wait()
    assert cursor != cache[-1]['id'], cursor
    try:
        for index, m in enumerate(cache):
           if m['id'] == cursor:
               return {'messages': cache[index + 1:]}
        return {'messages': cache}
    finally:
        if cache:
            session['cursor'] = cache[-1]['id']
        else:
            session.pop('cursor', None)

@route('/static/:filename', name='static')
def static_files(filename):
    return static_file(filename, root='./static/')

def create_message(from_, body):
    data = {'id': str(uuid.uuid4()), 'from': from_, 'body': body}
    data['html'] = template('message', message=data)
    return data

if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, server='gevent')
