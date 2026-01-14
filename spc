#!/usr/bin/env python3

from __future__ import print_function
import os
import subprocess
import sys
from builtins import input


def setup_virtualenv():
    os.system('python3 -m venv venv')
    os.system('./venv/bin/pip install -r ./requirements.txt')

def pass_to_cli(arg):
    path = './venv/bin/python'
    if os.path.exists(path):
        p = subprocess.Popen([path, 'src/main.py'] + arg)
        p.wait()
    else:
        print("ERROR: need to first setup environment by running ./spc init")


# give some usage info if user simply types ./spc
if len(sys.argv) < 2: sys.argv.append("help")

if sys.argv[1] == "requirements":
    setup_virtualenv()
elif sys.argv[1] == "init":
    user_input = input('Download dependencies and setup virtual environment? [Yn] ') or 'y'
    if user_input.lower() == 'y':
        setup_virtualenv() 
        pass_to_cli(['init']) 
else:
    pass_to_cli(sys.argv[1:])

