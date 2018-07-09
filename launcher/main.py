from Alfred.core.external.Qt import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget

import os
from bolt.core import qtCore
from bolt.core import mayaCore

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep
uiPath = os.path.dirname(os.path.realpath(__file__)) + os.sep + "ui" + os.sep


def show():
    '''Start an instance of the Module info UI'''
    # Launch an instance of the window
    global aModuleInfo
    boldLauncherWindow = bolt_launcher(parent=mayaCore.get_maya_Window())
    # Show the window
    boldLauncherWindow.show(dockable=True, floating=True)

class bolt_launcher(MayaQWidgetDockableMixin, QtWidgets.QDialog):
ste    '''Instance a module-menu that loads all of the modules from the Alfred.Modules folder'''
    def __init__(self, parent=None):
        super(bolt_launcher, self).__init__(parent)
        try: boldLauncherWindow.close()
        except: pass

        # UI loading
        print "{}boltMainUI.ui".format(uiPath)
        self.ui = qtCore.qtUiLoader("{}boltMainUI.ui".format(uiPath))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.resize(300, 240)
        # Create window attributes
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)


