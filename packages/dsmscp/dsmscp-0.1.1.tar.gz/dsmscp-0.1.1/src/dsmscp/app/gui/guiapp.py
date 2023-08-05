'''
Created on 19 avr. 2021

@author: tm
'''

import sys
from PyQt5.QtWidgets import QApplication, QErrorMessage
from .MainWindow import MainWindow


class GuiApp(object):
    """Main class of the module
    """
    def __init__(self, config=None):
        '''
        Constructor
        '''
        self.app = QApplication(sys.argv)
        self.config = config
        
    def start(self):
        """start the app
        """
        self.window = MainWindow(self.config)
        self.window.show()
        
        self.app.exec_()
        
    def displayError(self, error):
        '''Display the given error
        
        :param str error: The error message''' 
        error_dialog = QErrorMessage()
        error_dialog.showMessage(error)
        
        error_dialog.exec_()
        
    def handleError(self, exception):
        '''Handling an error or exception
        :param Exception e: the exception to be processed
        '''
        txt = str(exception)
        self.displayError(txt)
        
    def stop(self):
        pass
        