from functools import wraps
from bottle import request, response

class FlashPlugin(object):
    name = 'flash'

    def __init__(self, key='flash', secret=None):
        self.key = key
        self.secret = secret
        self.app = None
        #self.api = 2
        response.flash_messages = []

    def setup(self, app):
        self.app = app
        self.app.add_hook('before_request', self.load_flashed)
        self.app.add_hook('after_request', self.set_flashed)
        self.app.flash = self.flash
        self.app.get_flashed_messages = self.get_flashed_messages

    def load_flashed(self):
        m = request.get_cookie(self.key, self.secret)
        if m is not None:
            response.flash_messages = [m]

    def set_flashed(self):
        if hasattr(response, 'flash_messages'):
            response.set_cookie(self.key, response.flash_messages, self.secret)
            delattr(response, 'flash_messages')

    def flash(self, message, level=None):
        if not hasattr(response, 'flash_messages'):
            response.flash_messages = []
        response.flash_messages.append((message, level))

    def get_flashed_messages(self):
        if hasattr(response, 'flash_messages'):
            m = response.flash_messages
            delattr(response, 'flash_messages')
            response.delete_cookie(self.key)
            return m
            
    def apply(self, callback, context):
        return callback

