#!/usr/bin/env python

import os
import subprocess
import sys


if sys.argv[1] == "requirements":
    os.system('virtualenv venv')
    os.system('./venv/bin/pip install -r ./requirements.txt')
else:
    p = subprocess.Popen(['./venv/bin/python', 'src/main.py'] + sys.argv[1:])
    p.wait()
