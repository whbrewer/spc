#!/usr/bin/env python3

from __future__ import print_function
import os
import subprocess
import sys
from builtins import input


def setup_virtualenv():
    os.system('python3 -m venv venv')
    os.system('./venv/bin/pip install -r ./requirements.txt')
    install_venv_entrypoint()

def install_venv_entrypoint():
    venv_python = os.path.abspath('./venv/bin/python')
    if not os.path.exists(venv_python):
        return
    entrypoint_path = os.path.abspath('./venv/bin/spc')
    repo_root = os.path.abspath('.')
    script = """#!{venv_python}
# -*- coding: utf-8 -*-
import os
import sys

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    os.chdir(repo_root)
    python_exe = os.path.join(repo_root, 'venv', 'bin', 'python')
    main_py = os.path.join(repo_root, 'src', 'main.py')
    os.execv(python_exe, [python_exe, main_py] + sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
""".format(venv_python=venv_python, repo_root=repo_root)
    with open(entrypoint_path, 'w') as f:
        f.write(script)
    os.chmod(entrypoint_path, 0o755)

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
        print("TIP: run `source venv/bin/activate` so you can run `spc` from anywhere")
else:
    pass_to_cli(sys.argv[1:])
