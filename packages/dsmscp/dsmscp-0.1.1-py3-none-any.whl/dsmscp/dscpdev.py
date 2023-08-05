'''

:author: T. Marti
:date: Created on 19 mars 2021
'''

import os
import sys
from dsmscp import app


if __name__ == '__main__':
    
    app.initial_dir = os.path.dirname(__file__) 
    
    app.prepareCfg()
    app.processCfg()
    
    app.application = app.GuiApp(app.config)
    
    try:
        app.application.start()
    except Exception as e:
        app.application.stop()
        app.application.handleError(e)
        sys.exit(1)