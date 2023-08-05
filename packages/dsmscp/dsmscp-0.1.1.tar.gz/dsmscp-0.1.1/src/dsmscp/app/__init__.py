'''
Created on 19 avr. 2021

@author: tm
'''
from .common import *

__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)
'''Appication version number'''

__ver__ = '{0:d}.{1:d}'.format(*VERSION)
'''Appication short version number'''


exit_code = 0
'''Application exit code''' 

application = None
'''The application itself'''

from .launcher import prepareCfg, processCfg
from . import utils

from .gui import *

log = None
'''The application logger'''

args_config = {}
'''The arguments given by INI file'''
config = None
'''The application configuration'''

initial_dir = None
'''The application initial directory. The folder of the main script.'''

parser = None
'''The argument line parser'''