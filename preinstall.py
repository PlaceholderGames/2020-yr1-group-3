import os
import sys
import subprocess
import pkg_resources
import platform
import main

required = {'pygame', 'pytmx'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

python = sys.executable


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if missing:
    for module in missing:
        subprocess.check_call([python, '-m', 'pip', 'install', module])

cls()
