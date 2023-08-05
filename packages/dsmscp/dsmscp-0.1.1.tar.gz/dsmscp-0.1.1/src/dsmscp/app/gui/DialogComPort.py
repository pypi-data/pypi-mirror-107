'''Module for class DialogComPort. This module implement a dialog for choosing a communication port. 

:author: T. Marti
:date: 2021-??-?? Creation
'''
from .ui_dialogcomport import Ui_dialog
from PyQt5.QtWidgets import QDialog

class DialogComPort(QDialog, Ui_dialog):
    """class for making a dialog windows for selecting the serial coomunication port
    
    :param list ports: list of available ports
    """
    def __init__(self, ports):
        super(DialogComPort, self).__init__()
        self.setupUi(self)
        self.portIndex = []
        self.portRef = []
        for p in ports:
            self.portIndex.append(str(p))
            self.portRef.append(p)
            self.comboBox.addItem(str(p))
            
    def getSelectedPort(self):
        """get the selected port of the dialog
        """
        return self.portRef[self.portIndex.index(self.comboBox.currentText())]