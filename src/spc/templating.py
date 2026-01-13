from __future__ import absolute_import

import os

from bottle import SimpleTemplate, TEMPLATE_PATH, template as bottle_template

from . import config

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))

try:
    SimpleTemplate.defaults["tab_title"] = config.tab_title
except Exception:
    SimpleTemplate.defaults["tab_title"] = "SPC"

SimpleTemplate.defaults.setdefault("app", "")
SimpleTemplate.defaults.setdefault("user", "")
SimpleTemplate.defaults.setdefault("status", "")
SimpleTemplate.defaults.setdefault("description", "")


def template(name, *args, **kwargs):
    return bottle_template(name, *args, **kwargs)
