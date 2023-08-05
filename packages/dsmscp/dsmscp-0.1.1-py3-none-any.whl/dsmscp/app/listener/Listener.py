'''Module for class Listener. This module implements the network socket communications remote Dassym's board and proxy. 

:author: T. Marti
:date: 2021-??-?? Creation
'''
import socket
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal


class Listener(QObject):
    """Listener of the proxy
    
    this class is made to be placed in a thread
    
    :param str host: proxy host name
    
    :param int port: proxy port number
    
    :param str initMsg: initialization message for the proxy (EX: "Dassym Tom Marti")
    """
    
    msgSignal = pyqtSignal(bytes)
    """Message signal, launch when the listener receive a message
    """
    
    logSignal = pyqtSignal(str)
    """Logging signal, launch when the listener have to log 
    """
    
    clsSignal = pyqtSignal()
    """Close signal, launch when the socket are closed by the proxy
    """
    
    connectedSignal = pyqtSignal()
    """Connected signal, launch when the socket are connected to the proxy
    """
    
    aliveSignal = pyqtSignal()
    """Alive signal, launch when the proxy want to now if the client is alive
    """
        
    def __init__(self, host, port, initMsg):
        QObject.__init__(self)
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        
        self.s.settimeout(1)
        
        self.write(initMsg)
        
    def write(self, data):
        """Write data on the socket
        
        :param bytes data: contain the data to send
        """
        if not isinstance(data, bytes):
            data = data.encode()
            
        self.logSignal.emit("Send " + str(data.decode()))
        self.s.send(data)

    def start(self):
        """Start the asyncore loop
        """
        self.logSignal.emit("Start handling msg")
        self.read()

        
        
    def read(self):
        """Read the socket and dispatch the received messages
        """
        noError = True
        while noError:
            try:
                msg = self.s.recv(1024)
            except socket.timeout as e:
                sleep(.01)
                continue
            except socket.error as e:
                # Something else happened, handle error, exit, etc.
                raise e
            else:
                if len(msg) == 0:
                    noError = False
                else:
                    # got a message do something :)
                    decodedMsg = msg.decode()
                    if decodedMsg == "ACK":
                        self.logSignal.emit("Receive ACK")
                        self.connectedSignal.emit()
                    elif decodedMsg == "alive":
                        self.logSignal.emit("Receive alive")
                        self.aliveSignal.emit()
                    elif decodedMsg == "authentificationerror":
                        self.logSignal.emit("Authentification error")
                    else:
                        self.msgSignal.emit(msg)
        
        # close the connection if the loop is exit
        self.close()
        
    def close(self):
        """Call by the loop when the proxy closed the connexion
        """
        self.logSignal.emit("Start closing socket")
        self.s.close()
        self.clsSignal.emit()
        
