import os

PIP_BIN = 'pip'
REQUIREMENTS_PIP = './requirements.pip'
VIRTUALENV_BIN = 'virtualenv'
VIRTUALENV_DIR = './venv'

try:
    del os.environ['PIP_RESPECT_VIRTUALENV']
except KeyError:
    pass

try:
    del os.environ['PIP_VIRTUALENV_BASE']
except KeyError:
    pass

try:
    os.mkdir(VIRTUALENV_DIR)
except OSError:
    pass

os.system('%s --distribute %s' % (VIRTUALENV_BIN, VIRTUALENV_DIR))
os.system('%s/bin/pip install -r %s' % (VIRTUALENV_DIR, REQUIREMENTS_PIP))
