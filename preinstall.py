import os
import sys
import subprocess
import pkg_resources
import platform

required = {'pygame', 'pytmx'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

python = sys.executable


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


# print("Checking for missing modules")
if missing:
    #print("Found", len(missing), 'missing modules')
    for module in missing:
    #  print("Installing", module)
        subprocess.check_call([python, '-m', 'pip', 'install', module])
    #  print("Installed", module)
else:
    pass
    # print("Found 0 missing modules")
    # print("Launching The Beerzerker")

cls()
subprocess.check_call([python, './main.py'])