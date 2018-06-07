from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg
import os
windowAnim = True

import pymel.core as pm

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep

def qtUiLoader(uifile, widget=None):
    ui = QtCompat.loadUi(uifile)  # Qt.py mapped function
    if not widget:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and \
                            member is not 'staticMetaObject':
                setattr(widget, member, getattr(ui, member))
        return ui



class fadeButton(QtWidgets.QToolButton):
    """Create star-icon on card """

    def __init__(self, parent):
        super(fadeButton, self).__init__()
        # QToolButton.__init__(self, parent)

        self.width = 20
        self.height = 20
        self.opacity = 0.3
        self.endOpacity = 0.7
        self.inAnimDuration = 300
        self.outAnimDuration = 800

        # Create opacity effect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)
        self.setOpacity(self.opacity)
        self.activeButton = False

        # Set sizing policy on button
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)

        # Set cursor
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # Set sizing of the button
        # self.setSize(self.width, self.height)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.setStyleSheet('''QToolButton {color: rgb(250, 250, 250);background-color: rgb(0, 250, 0,0);border-style: None;border-width: 0px;}QToolButton:menu-indicator { image: none; }''')

    def setOpacity(self, opacity):
        self.opacityEffect.setOpacity(opacity)
        self.opacity = opacity

    def setSize(self, width, height):
        self.setIconSize(QtCore.QSize(width, height))

        self.width = width
        self.height = height

    def enterEvent(self, event):
        if self.activeButton is False:
            qtCore.fadeAnimation(start="current", end=self.endOpacity, duration=self.inAnimDuration,
                                 object=self.opacityEffect)
            # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def leaveEvent(self, event):
        if self.activeButton is False:
            qtCore.fadeAnimation(start="current", end=self.opacity, duration=self.outAnimDuration,
                                 object=self.opacityEffect)
            # self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)


class valueButton(QtWidgets.QToolButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(valueButton, self).__init__()

        # Initialise value
        self.value = None
        self.multiple = False
        self.originalTitle = None


        # Create opacity effect
        self.opacity = 0.8
        self.endOpacity = 1
        self.inAnimDuration = 300
        self.outAnimDuration = 800
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)

        # Set style
        self.inactiveStyleSheet = "padding: 5px;border-radius: 5px;\nbackground-color: rgb(250,250,250,20);\ncolor: rgb(250,250,250,200);"
        self.activeStyleSheet = "padding: 5px;border-radius: 5px;\nbackground-color: rgb(0,153,51);\ncolor: rgb(250,250,250,200);"
        self.setStyleSheet(self.inactiveStyleSheet)
    def add_value(self):
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            #self.value = [object.name() for object in selection]
            valueName = [object.name() for object in selection]
            valueName = ",".join(valueName)[:(int(self.width() * 0.15))]

            self.set_value(selection, valueName=valueName)
            self.opacity = 1
            self.setStyleSheet(self.activeStyleSheet)

        else:
            #self.setText("No selection")
            #self.setStyleSheet("padding: 5px;border-radius: 5px;\nbackground-color: rgb(250,250,250,20);\ncolor: rgb(250,250,250,200);")
            self.opacity = 0.6

            activatePopup(self, "You dont have any selection")
            self.setStyleSheet(self.inactiveStyleSheet)
            self.set_value(None, valueName=self.originalTitle)
    def reset_value(self):
        self.setStyleSheet("")
    def set_value(self, value, valueName="Assigned"):
        height = self.size().height()
        width = self.size().width()

        # Set value in button
        self.value = value
        # Set text of button

        # Calculate new size

        self.setText(valueName)



        # Measure text
        metrics = QtGui.QFontMetrics(self.font())
        newWidth = metrics.width(valueName) + 20



        # Set color of button
        #self.setStyleSheet("padding: 5px;border-radius: 5px;\nbackground-color: rgb(0,153,51);\ncolor: rgb(250,250,250,200);")

        # Aninmate size
        #animateWidgetSize(self, start=(30, height), end=((width * 2), height),duration=3000,attributelist=("minimumSize"))
        #propertyAnimation(start=[0,height], end=[width,width], duration=600, object=self, property="minimumSize")
        propertyAnimation(start=[width,height], end=[newWidth,height], duration=600, object=self, property="maximumSize", mode="OutExpo")
        #propertyAnimation(start=[width, height], end=[newWidth, height], duration=600, object=self, property="minimumSize", mode="OutExpo")


    def set_text(self, input):
        self.setText(input)
        if self.originalTitle == None: self.originalTitle = input

        height = self.size().height()
        # Measure text
        metrics = QtGui.QFontMetrics(self.font())
        newWidth = metrics.width(input) + 20
        propertyAnimation(start=[(newWidth - 20), height], end=[newWidth, height], duration=500, object=self, property="maximumSize", mode="OutExpo")

    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def enterEvent(self, event):
        fadeAnimation(start="current", end=self.endOpacity, duration=self.inAnimDuration,object=self.opacityEffect)
        # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def leaveEvent(self, event):
        fadeAnimation(start="current", end=self.opacity, duration=self.outAnimDuration,object=self.opacityEffect)
        # self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)


class dropButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(dropButton, self).__init__()

        # Initialise value
        self.setAcceptDrops(True)
        self.value = None

    def add_value(self):
        print "Add a value to me"
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            self.value = selection
            #self.value = [object.name() for object in selection]
            valueName = [object.name() for object in selection]

            # Set text of button
            self.setText(",".join(valueName)[:(int(self.width() * 0.15))])

            # Set color of button
            self.setStyleSheet('background-color: rgb(250,250,250,200')

    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
            # Add highlight to window
            self.setStyleSheet('background-color: rgb(250,250,250,250')

    def dragLeaveEvent(self, e):
        # Reset highlight to window
        self.setStyleSheet('background-color: rgb(250,250,250,200')

    def dropEvent(self, event):
        # Reset highlight to window
        self.setStyleSheet('background-color: rgb(250,250,250,50')

        droppedCommand = event.mimeData().text()
        print droppedCommand
        print event.mimeData()


class pathButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(pathButton, self).__init__()

        # Initialise value
        self.value = None
        self.pathField = None

    def add_value(self):
        print "Add a value to me"
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            self.value = selection
            #self.value = [object.name() for object in selection]
            valueName = [object.name() for object in selection]

            # Set text of button
            self.setText(",".join(valueName)[:(int(self.width() * 0.15))])

            # Set color of button
            self.setStyleSheet('background-color: rgb(250,250,250,200')

    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def add_path(self):
        file = picker_dialog(mode="ExistingFile", filter="Maya file(*.mb)")
        print file
        if self.pathField != None:
            self.pathField.setText(file[0])

def get_value(object):
    '''Get the current value from a input field, numeric slider etc'''
    # Get type
    if type(object) == QtWidgets.QLineEdit:  #QLineEdit
        value = object.text()
    elif "valueButton" in str(type(object)):  #ValueButton
        value = object.get_value()
    elif "vectorInput" in str(type(object)):  #ValueButton
        value = object.get_values()
    elif type(object) == QtWidgets.QLabel:  #Label
        value = None
    elif type(object) == QtWidgets.QSpinBox:  #QSpineBox
        value = object.value()
    elif type(object) == QtWidgets.QDoubleSpinBox:  #QDoubleSpinBox
        value = object.value()
    elif type(object) == QtWidgets.QCheckBox:  #QCheckBox
        value = object.isChecked()
    elif type(object) == QtWidgets.QComboBox:  #QComboBox
        value = object.currentText()


    else:
        print "No supported type found for '{}'".format(type(object))
        value = None

    return value

def set_value(object, value):
    '''Get the current value from a input field, numeric slider etc'''
    # Get type
    print type(value)
    if type(object) == QtWidgets.QLineEdit:
        object.setText(value)
    elif type(object) == QtWidgets.QPushButton:
        object.set_value(value)
    elif type(object) == QtWidgets.QLabel:
        object.setText(value)
    elif type(object) == QtWidgets.QSpinBox:
        object.setValue()
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.setValue()
    elif type(object) == QtWidgets.QComboBox:
        object.setCurrentText(value)
    elif type(object) == QtWidgets.QCheckBox:
        object.isChecked(value)
    else:
        print "No supported type found for '{}'".format(type(object))
        value = None

    return value

def connect_value_change(object, connection=None):
    '''Connect the changecommand for a object based on its type'''
    if type(object) == QtWidgets.QLineEdit:
        object.textChanged.connect(connection)
    elif type(object) == QtWidgets.QPushButton:
        object.clicked.connect(connection)
    elif "valueButton" in str(type(object)):  # ValueButton
        object.clicked.connect(connection)
    elif type(object) == QtWidgets.QLabel:
        print "Setting connection on a label is not supported for now"
    elif type(object) == QtWidgets.QSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QComboBox:
        object.currentIndexChanged.connect(connection)
    elif type(object) == QtWidgets.QCheckBox:
        object.stateChanged.connect(connection)
    else:
        print "No supported type found for '{}'".format(type(object))


# Load the svg
def load_svg(iconPath, size=(20,20)):
    svg_renderer = QtSvg.QSvgRenderer(iconPath)
    image = QtGui.QImage(size[0], size[1], QtGui.QImage.Format_ARGB32)
    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))
    pixmap = QtGui.QPixmap.fromImage(image)
    icon = QtGui.QIcon(pixmap)

    return icon



def clearLayout(layout):
    '''Clear input layout of its content'''
    if layout != None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())


def autoFieldWidth(inputObject, offset=0, minimum=0):
    '''Takes any object that have a "text" attribute and sets its width according to its content'''
    text = inputObject.text()
    metrics = QtGui.QFontMetrics(inputObject.font())
    width = metrics.width(text) + offset
    #Set field
    if width <= minimum: width = minimum

    inputObject.setMaximumWidth(width)
    inputObject.setMinimumWidth(width)

def selectItemByIndex(listWidget, index):
    '''Select the index of a QListWidget'''
    firstItem = listWidget.item(index)
    listWidget.setCurrentItem(firstItem)


def select_item_by_text(listWidget, text):
    '''Select the index of a QListWidget'''
    if type(listWidget) == QtWidgets.QListWidget:
        items = [listWidget.item(i).text() for i in range(listWidget.count())]
        index = items.index(text)  # Get text's index
        if index != -1:
            listWidget.setCurrentRow(index)
        else:
            print "Index probably not found:"
            print "Input text", text
            print "Index found", index
    elif type(listWidget) ==  QtWidgets.QListWidget:
        index = listWidget.findText(str(text))
        listWidget.setCurrentIndex(index)
    else:
        print "No supported type provided for 'qtCore.select_item_by_text'"
        print "TYPE:", type(listWidget)



def centerWidgetOnScreen(widget):
    '''Center a given widget on the active screen'''
    frameGm = widget.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    widget.move(frameGm.topLeft())

def animateWidgetSize(element, start=(300, 100), end=(300, 150),expanding=False, attributelist=("minimumSize", "maximumSize"), duration=False):
    '''Animate an objects height'''

    if duration == False:
        duration = min(abs(start[1] - end[1]) * 5, 500)

    #duration = 0
    #for attribute in ["minimumSize", "maximumSize"]:
    for attribute in attributelist:
        if attribute == "minimumSize":
            element.setMinimumHeight(end[1])
        elif attribute == "maximumSize":
            element.setMaximumHeight(0)
            # pass

        # Create animation property and set start and end point
        animation = QtCore.QPropertyAnimation(element, attribute, element)
        if attribute == "maximumSize":
            animation.setStartValue(QtCore.QSize(6000, start[1]))
            animation.setEndValue(QtCore.QSize(6000, end[1]))
        else:
            animation.setStartValue(QtCore.QSize(0, start[1]))
            animation.setEndValue(QtCore.QSize(0, end[1]))

        # Create easing style
        style = QtCore.QEasingCurve()
        if start[1] <= end[1]:
            style.setType(QtCore.QEasingCurve.OutBounce)
            style.setAmplitude(0.2)

        else:
            style.setType(QtCore.QEasingCurve.InOutQuart)
        animation.setEasingCurve(style)

        if expanding == True:
            if start[1] <= end[1]:
                if attribute == "maximumSize":
                    [animation.finished.connect(x) for x in [lambda: element.setMaximumHeight(1699999), lambda: element.setMinimumHeight(0)]]

        # Set duration
        animation.setDuration(duration)

        # Start animation and delete when finished
        animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)


###################################################################################################
# Animation
###################################################################################################

def propertyAnimation(start=[0, 0], end=[30, 0], duration=300, object=None, property="iconSize",mode="InOutQuint"):
    animation = QtCore.QPropertyAnimation(object, property, object)
    # Easing

    style = QtCore.QEasingCurve()
    if mode == "Linear": style.setType(QtCore.QEasingCurve.Linear)
    elif mode == "InQuad": style.setType(QtCore.QEasingCurve.InQuad)
    elif mode == "OutQuad":style.setType(QtCore.QEasingCurve.OutQuad)
    if mode == "InOutQuad": style.setType(QtCore.QEasingCurve.InOutQuad)
    elif mode == "OutInQuad": style.setType(QtCore.QEasingCurve.OutInQuad)
    elif mode == "InCubic":style.setType(QtCore.QEasingCurve.InCubic)
    if mode == "OutCubic": style.setType(QtCore.QEasingCurve.OutCubic)
    elif mode == "InOutCubic": style.setType(QtCore.QEasingCurve.InOutCubic)
    elif mode == "OutInCubic":style.setType(QtCore.QEasingCurve.OutInCubic)
    if mode == "InQuart": style.setType(QtCore.QEasingCurve.InQuart)
    elif mode == "OutQuart": style.setType(QtCore.QEasingCurve.OutQuart)
    elif mode == "InOutQuart":style.setType(QtCore.QEasingCurve.InOutQuart)
    if mode == "OutInQuart": style.setType(QtCore.QEasingCurve.OutInQuart)
    elif mode == "InQuint": style.setType(QtCore.QEasingCurve.InQuint)
    elif mode == "InBounce":style.setType(QtCore.QEasingCurve.InBounce)
    elif mode == "OutExpo":style.setType(QtCore.QEasingCurve.OutExpo)
    elif mode == "InExpo": style.setType(QtCore.QEasingCurve.InExpo)
    elif mode == "InOutQuint": style.setType(QtCore.QEasingCurve.InOutQuint)
    elif mode == "OutBounce":
        style.setType(QtCore.QEasingCurve.OutBounce)
        style.setAmplitude(0.5)
    else:
        print "Mode not supported:",mode
        style.setType(QtCore.QEasingCurve.InOutQuint)


    animation.setEasingCurve(style)

    # Set Duration
    animation.setDuration(duration)

    # Set start values
    if start[0] == "current":
        startValueX = object.iconSize().height()
    else:
        startValueX = start[0]
    if start[1] == "current":
        startValueY = object.iconSize().width()
    else:
        startValueY = start[1]
    animation.setStartValue(QtCore.QSize(startValueX, startValueY))
    animation.setEndValue(QtCore.QSize(end[0], end[0]))
    animation.start()

    # Animate
    animation.start()

def fadeAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start is "current": start = object.opacity()
        if end is "current": end = object.opacity()

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, "opacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start()
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setOpacity(end)

def fadeWindowAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, "windowOpacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start()
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setWindowOpacity(end)
        if finishAction != None:
            object.close()

def resizeWindowAnimation(start=(0, 0), end=(0, 0), duration=300, object=None, finishAction=None,attribute="maximumHeight"):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start[0] == "current": start[0] = object.size().height()
        if start[1] == "current": start[1] = object.size().width()

        # Animate window opasity
        positionAnimation = QtCore.QPropertyAnimation(object, attribute, object)
        positionAnimation.setEasingCurve(style)
        positionAnimation.setDuration(duration)
        positionAnimation.setStartValue(QtCore.QSize(start[0], start[1]))
        positionAnimation.setEndValue(QtCore.QSize(end[0], end[1]))
        positionAnimation.start()

        if finishAction != None:
            positionAnimation.finished.connect(finishAction)
    else:
        object.resize(end[0], end[1])
        if finishAction != None:
            object.close()
    pass

def slideWindowAnimation(start=-100, end=0, duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, 'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning
        if start >= end:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x(), pos.y() + start))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x(), pos.y() + end))
        slideAnimation.start()




def slideWindowBothAnimation(start=(-100, 0), end=(0, 0), duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, 'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning

        if start[0] >= end[0]:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x() + start[1], pos.y() + start[0]))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x() + end[1], pos.y() + end[0]))
        slideAnimation.start()



###################################################################################################
# Dialogs
###################################################################################################

def yesCancelDialog(title="Remove action", message="Are you sure you wanna remove this action?"):
    # Create dialog
    saveCurrentDialog = QtWidgets.QMessageBox()
    saveCurrentDialog.setText(title)
    saveCurrentDialog.setInformativeText(message)
    saveCurrentDialog.addButton(QtWidgets.QMessageBox.No)
    saveCurrentDialog.addButton(QtWidgets.QMessageBox.Yes)

    # Execute dialog
    reply = saveCurrentDialog.exec_()
    if reply == QtWidgets.QMessageBox.Yes:
        reply = "Yes"
    if reply == QtWidgets.QMessageBox.No:
        reply = "Cancel"
    return reply

def saveDialog(title="Unsaved Action", message="Do you want to save your changes?", object=False):
    # Create dialog
    saveCurrentDialog = QtWidgets.QMessageBox()
    saveCurrentDialog.setText(title)
    saveCurrentDialog.setInformativeText(message)
    saveCurrentDialog.setStandardButtons(
        QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
    saveCurrentDialog.setDefaultButton(QtWidgets.QMessageBox.Save)
    # Execute dialog
    reply = saveCurrentDialog.exec_()
    if reply == QtWidgets.QMessageBox.Save:
        return "save"
    if reply == QtWidgets.QMessageBox.Discard:
        return "discard"
    if reply == QtWidgets.QMessageBox.Cancel:
        return "cancel"


def picker_dialog(mode="AnyFile", filter=None, message="Open file/folder"):
    '''Open a filePickerDialog and return the path to the object'''

    # Example on filter
    #"A - TEMPLATE(*.aTemplate)"

    # Create dialog
    dialog = QtWidgets.QFileDialog()

    # Set mode
    if mode == "AnyFile":
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    elif mode == "SaveFile":
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    elif mode == "ExistingFile":
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    elif mode == "Directory":
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    elif mode == "ExistingFiles":
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
    elif mode == "DirectoryOnly":
        print "Only directory"
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)


    # Set filter if asked for
    if filter != None:
        dialog.setNameFilter(filter)

    if "Directory" in mode:
        output = dialog.getExistingDirectory(None, message, filter=filter)
    elif mode == "SaveFile":
        output = dialog.getSaveFileName(None, message, filter=filter)[0]
    else:
        output = dialog.getOpenFileName(None, message, filter=filter)

    return output


def activatePopup(button, text, header="Info", icon="infoIcon"):
    window = button.parent().window()
    '''Create a popup object from the current sender'''
    global popup
    popup = info_popup(widget=window)
    popup.setText(text)

    popup.setHeader(header)
    popup.setIcon(icon)
    popup.show()

class info_popup(QtWidgets.QWidget):
    def __init__(self, parent = None, widget=None):
        super(info_popup, self).__init__()
        self.ui = qtUiLoader("{}popupCardSimple.ui".format(relativePath + os.sep + "ui" + os.sep))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        #self.frame.adjustSize()


        # Tag this widget as a popup
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)

        # calculate the botoom right point from the parents rectangle
        #point = widget.srect().bottomRight()
        #print point

        # Set image
        iconFile = load_svg((relativePath + os.sep + "icons" + os.sep + "plugIcon.svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

        # map that point as a global position
        global_point = QtGui.QCursor.pos()

        self.adjustSize()

        #Position based on the cursor
        self.move(global_point - QtCore.QPoint((self.width() * 3), 0))
        self.ui.closeButton.clicked.connect(self.hide)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)

        #self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)



    def hide(self):
        fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)
        slideWindowBothAnimation(start=(0, 0), end=(30, 0), duration=150, object=self)
        #self.deleteLater()

    def setText(self, text):
        self.ui.infoLabel.setText(text)

        # Calculate size
        # Measure text
        #metrics = QtGui.QFontMetrics(self.ui.infoLabel.font())
        #newWidth = metrics.width(text)

        # Set small size to the fill out with what it needs
        self.resize(20, 20)  # width, height


        #self.resi


        global_point = QtGui.QCursor.pos()
        #self.adjustSize()
        self.move(global_point - QtCore.QPoint((self.width()) - 10, self.height() - 10))
        slideWindowBothAnimation(start=(30, 0), end=(0, 0), duration=400, object=self)
        self.ui.infoLabel.adjustSize()

    def setHeader(self, text):
        self.ui.header.setText(text)

    def setIcon(self, text):
        # Set image
        iconFile = load_svg((relativePath + os.sep + "icons" + os.sep + text + ".svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

    def closeEvent(self, event):
        event.accept()
        fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)




class vectorInput(QtWidgets.QWidget):
    def __init__(self, parent = None, widget=None):
        super(vectorInput, self).__init__()
        self.ui = qtUiLoader("{}vectorWidget.ui".format(relativePath + os.sep + "ui" + os.sep))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Adjust size
        self.adjustSize()

    def get_values(self):
        value01 = self.ui.value01.value()
        value02 = self.ui.value02.value()
        value03 = self.ui.value03.value()

        return (value01, value02, value03)

    def set_values(self, value01, value02, value03):
        self.ui.value01.setValue(value01)
        self.ui.value02.setValue(value02)
        self.ui.value03.setValue(value03)

class QHLine(QtWidgets.QFrame):
    '''Class to make a horizontal line break'''
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


###################################################################################################
# Handle QTreeWidget/QTreeWidgetItems
###################################################################################################
def get_children_from_treeWidgetItem(treeWidgetItem):
    '''Return all items from a qTreeWidgetItem'''
    items = [treeWidgetItem.child(number) for number in xrange(treeWidgetItem.childCount())]

    return items

def remove_children_from_treeWidgetItem(treeWidgetItem):
    '''Remove all the children from a QTreeWidgetItem'''

    for item in reversed(range(treeWidgetItem.childCount())):
        treeWidgetItem.removeChild(treeWidgetItem.child(item))