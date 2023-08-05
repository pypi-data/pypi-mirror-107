'''Module for class MainWindow. This module implement the graphical and logical for the dsm-scp. 

:author: T. Marti
:date: 2021-??-?? Creation
'''
from PyQt5 import QtWidgets
import time
import serial
from serial.tools import list_ports
import datetime as DT
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os

import dapi2
import dboard
from dapi2.dmsg.message import BaseMessage
from dapi2.common import DApi2Side
from dapi2.dmsg.writer import MsgWriter

from .ui_mainwindow import Ui_MainWindow
from ..listener.Listener import Listener
from .DialogComPort import DialogComPort
from ..utils import File

        
        
class MainWindowWidgetManager(QtWidgets.QMainWindow, Ui_MainWindow):
    """Class for making a Qt main window
    
    :param * args: arguments
         
    :param ** kwargs: arguments but with an index
    """
    def __init__(self, *args, **kwargs):
        super(MainWindowWidgetManager, self).__init__(*args, **kwargs)
        
        self.dirPath = os.path.dirname(os.path.realpath(__file__))
        self.imagePath = self.dirPath + "/../../img/"
        
        self.setWindowTitle('Dassym - Slave Control Panel')
        iconPath = self.imagePath + 'dassym-icon.png'
        self.setWindowIcon(QIcon(iconPath))
        
        self.proxyHost = ""
        self.proxyPort = 0
        
        self.setupUi(self)
        
        self.consoleText = ""
                
        # button linker
        self.buttonConnexion.clicked.connect(self.onButtonConnexionClicked)
        self.actionauto_connect.triggered.connect(self.onAutoConnectTriggered)
        self.setConnexionStatus(False)
           
      
    def onButtonConnexionClicked(self):
        """Abstract function for handle event button clicked 
        """
        assert False
        pass
    
    def onAutoConnectTriggered(self):
        assert False
        pass
        
    def putInConsole(self, msg):
        """put a message in console object in log format
        
        :param str msg: msg to put on console
        """
        self.consoleText = time.strftime('%a %H:%M:%S') + ":  " + msg + "\n" + self.consoleText
        self.textConsole.setText(self.consoleText)
        self.update()
        
    def setConnexionStatus(self, connected=True):
        text = None
        icon = self.imagePath
        
        if connected:
            icon += "dot-green.svg"
            text = 'Connected to proxy @ {}:{}'.format(self.proxyHost, self.proxyPort)
        else:
            icon += "dot-red.svg"
            text = 'Disconnected from proxy'
            
        self.proxyStatus.setText(text)
        self.proxyStatusImage.setPixmap(QPixmap(icon).scaled(15, 15))
        
    def setButtonConnexionEnabled(self, state=True):
        """enable or disable connection button
        
        :param bool state: want to enable ?
        """
        self.buttonConnexion.setEnabled(state)
        self.update()
            
    def setButtonConnexionDisabled(self):
        """disable connection button
        """
        self.setButtonConnexionEnabled(False)

    def setInputEnabled(self, state=True):
        """enable or disable text input
        
        :param bool state: want to enable ?
        """
        self.inputEntreprise.setEnabled(state)
        self.inputFirstname.setEnabled(state)
        self.inputLastname.setEnabled(state)
        
    def setInputDisabled(self):
        """disable text input
        """
        self.setInputEnabled(False)
        
    def enableInterface(self, state=True):
        """enable or disable interface for the user action
        
        :param bool state: want to enable ?
        """
        self.setButtonConnexionEnabled(state)
        self.setInputEnabled(state)
        
    def disableInterface(self):
        """disable all interface for user action
        """
        self.enableInterface(False)


def wordToDate(value):
    '''Converts date encoded in a 16-bits (word) integer to Date.
    
    :param int value: The date  encoded in a word.
    :return: The converted Date, if *value* is between 1 and 65534, otherwise None.   
    :rtype: Date
    '''  
    if value==0 or value==0xffff: 
        return None
    else:
        try:
            return DT.date( 2000+((value & 0xfe00)//0x200), (value & 0x1e0)//0x20, (value & 0x1f) )
        except ValueError:
            return None

def wordToVersion(value):
    '''Converts  16-bits (word) integer to major and minor version number.
    
    :param int value: The word to convert
    :return: The version number in 2-tuple of integer.
    :rtype: tuple
    '''
    return (value >> 8, value & 0xFF)   

def versionToStr(ver):
    '''Converts version to str.
    
    :param tuple ver: The version tuple with major and minor number to convert.
    :return: The version in format n.mm
    :rtype: str
    '''
    return "{0:d}.{1:02d}".format(*ver)


class MainWindow(MainWindowWidgetManager):
    """Class for making a main window
    """
    def __init__(self, config=None):
        super().__init__()
        
        
        configFile= self.dirPath + "/../conf.txt"
        self.confFile = File(configFile)
        self.selectCom = False
        self.automaticReconnect = True
        
        self.config = config
        if self.config.host is not None:
            self.proxyHost, self.proxyPort = self.config.host.split(":")
        else:
            raise Exception("No host defined. add [-H host:port] at the end of the command")
        
        self.loadConf()
        self.initBoard()
        
        self.writer = MsgWriter(DApi2Side.MASTER)
        
        
    def initBoard(self, port=None):
        """init all the components for the board and the board itself
        """

        # select the port
        if port is None:
            ports = list(list_ports.comports())
            if len(ports) == 1:
                port = ports[0]
            if len(ports) > 1:
                self.selectSerial(ports)
                return
        
        # raise exception if no port have been choose
        if port is None:
            raise Exception("No serial port detected") 
        
        # make the communication between the pc and the board
        self.serial = serial.Serial(port[0], timeout=1)
        self.comm = dapi2.DSerial(self.serial)
        self.api = dapi2.DApi2(self.comm)
                
        # try to connect to the board
        try:
            self.board = dboard.DBoardFactory(self.api)
        except:
            raise Exception("Cannot connect to the board (connect or power on the board).") from None
        
        # extract the board informations
        self.board.getRegisters('system')
        self.board.getRegisters('psvr','wer', refresh=True)
        
        # create the board informations string
        serialStatus = "SN: {snr:05d}\nDate: {fdr:s}\nHardware: {hvr:s}\nFirmware: {svr:s}\nDate: {fbdr:s}\nBIOS: {bvr:s}\nDate: {bbdr:s}".format(
            snr=self.board.regs.snr.value,
            fdr=wordToDate(self.board.regs.fdr.value).isoformat(),
            hvr=versionToStr(wordToVersion(self.board.regs.hvr.value)),
            svr=versionToStr(wordToVersion(self.board.regs.svr.value)),
            fbdr=wordToDate(self.board.regs.fbdr.value).isoformat(),
            bvr=versionToStr(wordToVersion(self.board.regs.bvr.value)),
            bbdr=wordToDate(self.board.regs.bbdr.value).isoformat()
        )
        self.boardinfos.setText(serialStatus)
        
        # make the status bar of the serial connection to the board
        self.statusBar().showMessage("Connected to {board:s} from {serial:s} @ {speed:s} bauds".format(
                board="MB{}".format(self.board.number),
                serial=self.serial.port,
                speed=str(self.serial.baudrate)
            ))
                
    def selectSerial(self, ports):
        """Launch a dialog for selecting the serial communication port
        
        :param list ports: the list of ports to put in the box
        """
        dialog = DialogComPort(ports)
        r = dialog.exec()
        if r == True:
            self.initBoard(dialog.getSelectedPort())
        else:
            sys.exit(0)
        
    def startListener(self, msg):
        """Start the message listener and put it into its thread
        
        :param str msg: message to send to the proxy for initializing connection
        """
         
        # if the listener cannot connect to proxy, throw an exception
        try:
            self.listener = Listener(self.proxyHost, int(self.proxyPort), msg.encode())
        except Exception:
            raise Exception("no internet connection") from None
            
        self.thread = QThread()  
        self.listener.moveToThread(self.thread)
        self.thread.started.connect(self.listener.start)
        self.listener.msgSignal.connect(self.msgCallback)
        self.listener.logSignal.connect(self.logCallback)
        self.listener.clsSignal.connect(self.clsCallback)
        self.listener.aliveSignal.connect(self.aliveCallback)
        self.listener.connectedSignal.connect(self.connectCallback)
        self.thread.start()
        
    def onButtonConnexionClicked(self):
        """handle when the button <<connection>> is clicked
        initialize the connection
        """
        entreprise = self.inputEntreprise.text()
        firstname = self.inputFirstname.text()
        lastname = self.inputLastname.text()
        if entreprise != "" and firstname != "" and lastname != "":
            self.storeConf()
            msg = "{}:/:{}:/:{}".format(entreprise, firstname, lastname)
            self.disableInterface()
            self.consoleText = ""
            self.putInConsole("Initialization of the connection")
            self.startListener(msg)
            
    def onAutoConnectTriggered(self):
        self.automaticReconnect = not self.automaticReconnect
                
    def loadConf(self):
        """read the config file and initialize variable
        """
        confFromFile = self.confFile.read()
        if len(confFromFile):
            self.inputEntreprise.setText(confFromFile[0])
            self.inputFirstname.setText(confFromFile[1])
            self.inputLastname.setText(confFromFile[2])
            
    def storeConf(self):
        """store the params of the socket connexion
        """
        self.confFile.write(self.inputEntreprise.text() + "\n" + self.inputFirstname.text() + "\n" + self.inputLastname.text())
            
    def connectCallback(self):
        """Set the connexion status to connected
        """
        self.setConnexionStatus(True)
        
    def aliveCallback(self):
        """Reply to the server if the application is alive
        """
        self.listener.write("ACK".encode())
        
    def msgCallback(self, msg):
        """Transfer message to the board and board response to the proxy.
        
        call by the listener thread signal msg
        
        :param bytes msg: message receive on the socket
        """
        
        self.putInConsole("Receive {}".format(msg.decode()))
        
        message = BaseMessage.factoryRaw(bytearray.fromhex(msg.decode('ascii')), DApi2Side.MASTER)

        res = self.api.sendMessage(message)
                
        smsg = self.writer.encodeSocket(res)

        # self.putInConsole("send {}".format(smsg.buffer.decode()))
        
        self.listener.write(smsg)
        
    def logCallback(self, msg):
        """Add a message into the console object
        
        call by the listener thread signal when it want to log something
        
        :param str msg: message to put in console
        """
        self.putInConsole(msg)
        
    def clsCallback(self):
        """Close the connection and terminate the thread
        
        call by the listener when the socket is close by the proxy
        """
        self.putInConsole("Close proxy")
        self.thread.quit()
        self.thread.wait()
        self.enableInterface()
        self.setConnexionStatus(False)
        if self.automaticReconnect:
            self.onButtonConnexionClicked()
        
        