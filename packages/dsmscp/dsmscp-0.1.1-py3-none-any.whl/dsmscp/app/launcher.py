'''
Created on 10 mars 2021

@author: tm
'''
import argparse
import configparser
import os
import logging.handlers
import sys

import dapi2
from .utils import tr
from dsmscp import app

def prepareCfg():
    parser0 = argparse.ArgumentParser(description='{0:s} (v{1:s})'.format(app.NAME, app.__version__), add_help=False)
    parser0.add_argument("-c", "--config", dest="config", help = tr("Configuration file (.ini)") )
    # parser0.add_argument("--no-gui", dest="no_gui", action='store_true', default=False, help = tr("If present start no GUI application") )  
    parser0.add_argument("--qt5-options", dest="qt5_options", help = tr("Qt5 options") )
    parser0.add_argument("--lang", dest="lang", help=tr("ISO name of language to use."))
    
    app.config, remaining_argv0 = parser0.parse_known_args() #@UnusedVariable
    
    if app.config.config is not None:
        
        if os.path.dirname(app.config.config) == '':
            app.config.config = os.path.join(app.initial_dir, app.config.config )
        
        if not os.path.exists(app.config.config):
            raise Exception(tr("Configuration file not found!"))
        cfg = configparser.ConfigParser()
        cfg.read(app.config.config,encoding='utf_8_sig')  

        for section in cfg.sections() :
            if section == 'GLOBAL':
                prefix = ''
            else:
                prefix = section.lower()+'_'
            for k in cfg[section]:
                v = cfg[section][k]
                if v.lower() in ('yes', 'true'):
                    v = True
                elif v.lower() in ('no', 'false'):
                    v = False
                
                app.args_config[prefix+k] = v

    app.parser = argparse.ArgumentParser( parents=[parser0] )
    
    
    app.parser.add_argument("-l", "--log-level", dest="loglevel", choices=[ 'error', 'warning', 'debug', 'info', 'noset'], help=tr("Log level. (default = info)"), default="info"   )
    app.parser.add_argument("--log-file", dest="logfile", default='stderr', help=tr("LOG file (default = stderr)") )
    app.parser.add_argument("--log-max-size", dest="log_maxbytes", help=tr("Maximum LOG file size in bytes (default=100000)."), default=100000)
    app.parser.add_argument("--log-backup-count", dest="log_backupcount", help=tr("Number of LOG files retained (default=10)."), default=10)
    
    app.parser.add_argument("-S", "--serial", dest="serial", help=tr("Serial port for direct control."), metavar="SERIAL")
    app.parser.add_argument("-H", "--host", dest="host", help=tr("Host name and port for remote control. (host:port)"), metavar="HOST")
    
    app.parser.add_argument("-b", "--baudrate", dest="baudrate", type=int, help=tr("Baud rate. (default : {0})".format(dapi2.COM_SPEEDS[0]) ), metavar="BAUDRATE", default=dapi2.COM_SPEEDS[0])
    
    app.parser.add_argument("-v", "--version", action='version',  help=tr("Show software version"), version='%(prog)s version {0:s}'.format(app.__version__)   )

def processCfg():
    app.parser.set_defaults(**app.args_config)
    app.config = app.parser.parse_args()
    
    
    if app.config.loglevel:
        app.config.loglevel = getattr(logging, app.config.loglevel.upper())
    
    app.log = logging.getLogger()
    
    if app.config.logfile is None or app.config.logfile == 'stderr':
        log_handler = logging.StreamHandler(sys.stderr)
    elif app.config.logfile == 'stdout':
        log_handler = logging.StreamHandler(sys.stdout)
    else:
        if os.path.dirname(app.config.logfile) != '':
            logfile = os.path.normpath(app.config.logfile)
        else:
            logfile = os.path.normpath(os.path.join(app.DEFAULT_LOG_DIR, app.config.logfile))
            
        log_handler = logging.handlers.RotatingFileHandler( filename=logfile, maxBytes=app.config.log_maxbytes, backupCount=app.config.log_backupcount)

    app.log.setLevel(app.config.loglevel)
    logfmt = logging.Formatter(app.LOG_FORMAT)
    log_handler.setFormatter(logfmt)   
    app.log.addHandler(log_handler)
                