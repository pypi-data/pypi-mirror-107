import sys
import subprocess
import sys
import click
import os
import errno


def moduleIsNotExist(name):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed = [r.decode().split('==')[0] for r in reqs.split()]
    if name not in installed:
        return True
    return False

def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == errno.ENOENT:
            return False
    return True

def addModule(name):
    if moduleIsNotExist('poetry') and not is_tool('poetry'):
        os.system('pip install poetry')
    click.secho("install {} ....".format(name), fg='blue')
    os.system('poetry add {}'.format(name))




    
