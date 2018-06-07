from maya import OpenMayaUI
from external.Qt import QtWidgets

#Shiboken
try:
    from shiboken import wrapInstance
    import shiboken
except:
    from shiboken2 import wrapInstance
    import shiboken2 as shiboken


def get_maya_Window():
    '''Return the main maya-window as an instance to parent to'''
    window = OpenMayaUI.MQtUtil.mainWindow()
    mayaWindow = shiboken.wrapInstance( long( window ), QtWidgets.QMainWindow)
    return mayaWindow

