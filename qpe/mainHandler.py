import pandas as pd

from qpe.interface.interfaceHandler import InterfaceHandler
from qpe.content.contentHandler     import ContentHandler

class MainHandler( InterfaceHandler, ContentHandler ):
    def __init__(self, parent=None):
        InterfaceHandler.__init__(self)
        ContentHandler.__init__(self)