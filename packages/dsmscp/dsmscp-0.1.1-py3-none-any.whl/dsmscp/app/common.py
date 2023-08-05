from os.path import os
import sys


MAJOR_VERSION = 0
'''Major version number'''

MINOR_VERSION = 0
'''Minor version number'''

REVISION_VERSION = 1
'''Revision version number'''

VERSION = (MAJOR_VERSION, MINOR_VERSION, REVISION_VERSION)
'''Version number as 3-tuples containing *major*, *minor* and *revision* numbers.''' 


NAME = 'dsmcp'
'''Application name'''

DASSYM = 'Dassym'
'''Application editor'''

DASSYM_DOMAIN = 'dassym.com'
'''Application domain'''

TEMP_DIR = os.getenv('TMP') if os.name == 'nt' else '/tmp'
'''Path to temporary directory'''
#TODO: TEMP_DIR pour darwin 

DEFAULT_LOG_DIR = TEMP_DIR 
'''Path to deefault directory to store log file.'''

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
'''Format pattern for logging message'''


DIR = os.path.dirname(os.path.realpath(__file__))
'''Directory of application package'''

IMG_DIR = os.path.join( DIR, "..", "img")
'''Directory of application iamges'''

DATA_DIR = os.path.join( DIR, "..", "data")
'''Directory of application data'''

FIRM_DIR = os.path.join( DIR, "..", "firm")
'''Directory of Dassym's board firmware'''

USR_HOME_DIR = os.path.expanduser("~")
'''User home directory.'''


USR_DATA_DIR = os.path.join(USR_HOME_DIR, ".config","dassym") if sys.platform == 'linux' \
        else os.path.join(os.getenv('LOCALAPPDATA'), "Dassym") if sys.platform[:3] == 'win' \
        else os.path.join(USR_HOME_DIR, 'Library', 'Application Support', 'Dassym') if sys.platform[:6] == 'darwin' \
        else None
'''User Dassym directory.'''
        
USR_DATA_APP_DIR = os.path.join(USR_DATA_DIR, NAME)
'''Application User Dassym directory.'''    

resource_paths = {
    'user' : USR_DATA_DIR,
    'data' : DATA_DIR,
    'img'   : DATA_DIR,
    'firm'   : FIRM_DIR,
    }
'''Search paths for resource'''



