__version__ = "0.5"
__author__ = "Martin Gunnarsson (hello@deerstranger.com)"

import qtCore
from qtCore.external.Qt import QtWidgets, QtCore, QtGui

reload(qtCore)
reload(qtCore.animation)
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import os, re
import inspect

# External
import mayaCore


relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep
parentPath = os.path.abspath(os.path.join(relativePath, os.pardir))

reload(mayaCore)



def show():
    '''Start an instance of the Function-finder UI'''
    # Launch an instance of the window
    global bolt_launcher_instance
    bolt_launcher_instance = main_window(parent=qtCore.context_maya.get_window())
    # Show the window
    bolt_launcher_instance.show(dockable=True, floating=True)
    #


class main_window(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    '''Instance a module-menu that loads all of the modules from the Alfred.Modules folder'''
    def __init__(self, parent=None):
        super(main_window, self).__init__(parent)
        try: bolt_launcher_instance.close()
        except: pass

        self.functionDictionary = []
        self.attribute_objects = []
        self.window_state = "search"
        self.reset_text = True

        # UI loading
        self.ui = qtCore.qtUiLoader("{}launcher_interface.ui".format(relativePath))

        self.ui.properties_frame.setMaximumWidth(0)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.resize(350, 450)

        # Window attributes
        self.dockedMode = False
        self.setWindowTitle("Bolt " + str(__version__))
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.FramelessWindowHint)

        # Load functions by default
        self.load()

        # Button connections
        self.ui.runButton.clicked.connect(self.run)
        self.ui.functionList.itemPressed.connect(self.add_attributes)
        self.ui.reloadButton.clicked.connect(self.load)
        self.ui.resetAssignment.clicked.connect(lambda: self.add_attributes(change_state=False))
        self.ui.back_button.clicked.connect(self.change_state)

        self.ui.back_button.setHidden(True)

        self.setFocus()

        # Add keyboard shortcuts
        self.ui.settings_button.setIcon(qtCore.load_svg((relativePath + os.sep + "icons" + os.sep + "settings.svg"), size=(20, 20)))
        self.ui.reloadButton.setIcon(qtCore.load_svg((relativePath + os.sep + "icons" + os.sep + "reload.svg"), size=(20, 20)))

    def keyPressEvent(self, event):

        key = event.key()

        if key == QtCore.Qt.Key_Left:
            print "Left Key triggered"
            self.show_search()
        elif key == QtCore.Qt.Key_Right:
            self.add_attributes()
            print "Right Key triggered"
        elif key == QtCore.Qt.Key_Down:
            if self.ui.properties_frame.size().width() == 0:
                self.ui.functionList.blockSignals(True)
                self.changeListIndex(1)
                self.ui.functionList.blockSignals(False)
                self.reset_text = True
            else:
                print "Traverse properties frame down"
        elif key == QtCore.Qt.Key_Up:
            if self.ui.properties_frame.size().width() == 0:
                self.ui.functionList.blockSignals(True)
                self.changeListIndex(-1)
                self.ui.functionList.blockSignals(False)
                self.reset_text = True
            else:
                print "Traverse properties frame up"
        elif key == QtCore.Qt.Key_Backtab or key == QtCore.Qt.Key_Backspace:
            print "You pressed back-tab"
            self.ui.filterInput.setText("")
            self.filter_functions()
        elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            print "You pressed enter key"
            if self.ui.properties_frame.size().width() != 0:
                self.run()
            else:
                self.add_attributes()

        elif key == QtCore.Qt.Key_Escape:
            self.close()
        else:
            if self.ui.properties_frame.size().width() == 0:
                if self.reset_text:
                    self.ui.filterInput.setText(event.text())
                    self.reset_text = False
                else:
                    self.ui.filterInput.setText(self.ui.filterInput.text() + event.text())
                self.filter_functions()
            return event

    def show_search(self):

        if self.ui.search_frame.size().width() == 0:
            self.change_state()

            self.ui.filterInput.setText("")
            self.ui.filterInput.setFocus()

    def change_state(self):
        if self.window_state == "search":
            self.window_state = "attributes"
            # Get current size
            outItem = self.ui.search_frame
            inItem = self.ui.properties_frame

            self.ui.back_button.setHidden(False)
            qtCore.propertyAnimation(start=[0, 30], end=[30, 30], duration=600, object=self.ui.back_button, property="minimumSize", mode="OutExpo")
            qtCore.propertyAnimation(start=[0, 30], end=[200, 200], duration=600, object=self.ui.back_button, property="maximumSize", mode="OutExpo")
        else:
            self.window_state = "search"
            outItem = self.ui.properties_frame
            inItem = self.ui.search_frame

            qtCore.propertyAnimation(start=[30, 30], end=[0, 400], duration=600, object=self.ui.back_button,property="minimumSize", mode="OutExpo")
            qtCore.propertyAnimation(start=[100, 30], end=[0, 400], duration=600, object=self.ui.back_button,property="maximumSize", mode="OutExpo")

        width = outItem.size().width()
        height = outItem.size().height()

        qtCore.animateWidgetSize(outItem, start=(width, height), end=(0, height), duration=600, attributelist=("maximumSize", "minimumSize"), bounce=False)

        qtCore.animateWidgetSize(inItem, start=(0, height), end=(width, height), duration=600, attributelist=("maximumSize", "minimumSize"), expanding=True, bounce=False)

    def changeListIndex(self, input):
        # Get current index from item
        currentItem = self.ui.functionList.currentItem()
        self.ui.functionList.blockSignals(True)

        if self.ui.functionList.count() >= 1:
            currentIndex = self.ui.functionList.indexFromItem(currentItem)

            # Get index from QListWidgetItem
            currentNumber = currentIndex.row()

            # Get new item and set as current
            if ((currentNumber + input) >= 0):
                if (currentNumber + input + 1) >= (self.ui.functionList.count() + 1):
                    # Last item, set to first again
                    newItem = self.ui.functionList.item(0)
                else:
                    hidden = True
                    while hidden == True:
                        newItem = self.ui.functionList.item(currentNumber + input)
                        hidden = newItem.isHidden()
                        if hidden == True:
                            #input = input + input
                            if input >= 1:
                                input = input + 1
                            else:
                                input = input - 1
                        else:
                            # Check that not a header
                            card = newItem.data(109)
                            if "card_simple_ui" in str(type(card)):
                                continue
                            else:
                                hidden = True
                                if input >= 1:
                                    input = input + 1
                                else:
                                    input = input - 1
                                # if input == 1:
                                #     input = input + input
                                # else:
                                #     input = input - 1

                    # Check if new item is not a header
            if ((currentNumber + input) == -1):
                # Select the last item from the last item (count)
                newItem = self.ui.functionList.item(self.ui.functionList.count() - 1)
            self.ui.functionList.setCurrentItem(newItem)
            self.ui.functionList.blockSignals(False)

    def load(self):
        '''Trigger loading and reloading of the window'''
        # Block signals and clear layout
        reload(mayaCore)
        self.get_functions()
        self.get_arguments()
        reload(mayaCore)
        self.get_arguments()

        self.filter_functions()

    def run(self):
        '''Exexute from current existed function'''

        # Get active function
        currentItem = self.ui.functionList.currentItem()
        card = currentItem.data(109)
        functionName = card.getTitle()

        # Find function
        function = [x for x in self.functionDictionary if x[1] == functionName][0][0]

        # Get arguments from UI
        string = "mayaCore.{}(".format(functionName)
        argumentList = {}

        missingArguments = []
        for argument in self.arguments:
            # Reset color on label
            label = argument.property("label")
            label.setStyleSheet("color: rgb(200,200,200)")

            # If required, check if it have a value
            value = qtCore.get_value(argument)
            if argument.property("required"):
                # If no value
                if value == None:
                    missingArguments.append(argument)
            argumentList.update({argument.objectName():value})

        if len(missingArguments) == 0:
            #exec ("cmds.undoInfo(openChunk=True)")
            output = function(**argumentList)
            #try: function(**argumentList)
            #except Exception, errorMessage:
            #    print "ERROR WHEN RUNNING FUNCTION '{}': \n{}".format(functionName, errorMessage)
            #exec ("cmds.undoInfo(closeChunk=True)")

            #Reset UI if asked for
            if self.ui.resetOnRunCheckbox.isChecked():
                self.add_attributes()

        else:
            for argument in missingArguments:
                # Change label color
                label = argument.property("label")
                label.setStyleSheet("color: rgb(250,0,0)")

    def filter_functions(self):
        # Switch back to search ui if not active
        if self.window_state != "search":
            self.change_state()

        listWidget = self.ui.functionList

        # Get filter name
        filterQuery = self.ui.filterInput.text().lower().replace(" ", "")

        filterList = []
        headerNames = []
        header_items = []
        for number in xrange(listWidget.count()):
            # Get item
            item = listWidget.item(number)

            # Unhide all first
            item.setHidden(False)

            # Check that any result
            if len(filterQuery) >= 1:

                # Get card content
                card = item.data(109)

                # Continue if not a header
                if "card_simple_ui" in str(type(card)):
                    if filterQuery not in card.getTitle().lower().replace(" ", ""):
                        item.setHidden(True)
                    else:
                        filterList.append(item)
                        # Add name of headers to global
                        headerNames.append(item.data(100))
                else:
                    # If header
                    item.setHidden(True)
                    header_items.append(item)

        for item in header_items:
            # Get card content
            card = item.data(109)

            if card.get_title().lower() in headerNames:
                item.setHidden(False)


        # Set selected
        if len(filterList) != 0:
            self.ui.functionList.blockSignals(True)
            self.ui.functionList.setCurrentItem(filterList[0])
            self.ui.functionList.blockSignals(False)

    def add_attributes(self, change_state=True):
        # Define attribute layout
        attributeLayout = self.ui.attributeBox.children()[0]

        # Clear layout
        qtCore.clearLayout(attributeLayout)
        self.attribute_objects = []

        if change_state:
            self.change_state()

        # Create a layout for every input found
        if len(self.functionDictionary) >= 1:
            self.arguments = []
            currentItem = self.ui.functionList.currentItem()

            card = currentItem.data(109)
            functionName = card.getTitle()

            # Get function from list
            function = [x for x in self.functionDictionary if x[1] == functionName][0]

            # Create header
            headerLabel = QtWidgets.QLabel(functionName.capitalize().replace("_", " "))
            attributeLayout.addWidget(headerLabel)
            headerLabel.setStyleSheet("color: rgb(250,87,87)")

            # Create header
            headerLabelSmall = QtWidgets.QLabel("[{}]".format(functionName))
            attributeLayout.addWidget(headerLabelSmall)

            # Add Big font
            font = QtGui.QFont()
            font.setBold(True)
            font.setPointSize(14)
            headerLabel.setFont(font)

            # Add small font
            headerLabelSmall.setStyleSheet("color: rgb(250,250,250,100)")

            # Add docstring
            if function[1] != None:

                # Extract default from doc-string if they exists
                if function[2] != None:
                    if "{" in function[2]:
                        docString = function[2].split("{")[0]

                        # Get info from docString
                        extraInfo = eval("{" + function[2].split("{")[1])
                    else:
                        extraInfo = {"required":None}
                        docString = function[2]
                else:
                    extraInfo = {"required": None}
                    docString = "No info provided. Add a doc-string to show here."
                docStringLabel = QtWidgets.QLabel(docString)
                docStringLabel.setStyleSheet("color: rgb(250,250,250,200)")

                docStringLabel.setWordWrap(True)
                attributeLayout.addWidget(docStringLabel)
            else:
                extraInfo = {"required": None}

            # Add separator
            line = qtCore.QHLine()
            attributeLayout.addWidget(line)

            last_tab_object = None

            for key, value in function[3].iteritems():

                # Create layout
                layout = QtWidgets.QHBoxLayout()
                functionName = re.sub(r'([A-Z])', r' \1', key).capitalize()

                # Check if this plug is required
                if extraInfo["required"] != None:
                    if key in extraInfo["required"]:
                        functionName = functionName + "*"
                        required = True
                    else:
                        required = False
                else:
                    required = False


                # Create Label (formated nicely using re.sub and cap)
                textLabel = QtWidgets.QLabel(functionName.replace("_", " ") + ":")
                textLabel.setStyleSheet("color: rgb(200,200,200)")
                textLabel.setMinimumSize(100, 20)
                layout.addWidget(textLabel)

                # Variable for items to add to the layout
                valueObjects = []

                # Check so its not none
                if type(value) == str or type(value) == unicode:
                    # Special case for folders
                    if "file" in key:
                        valueObject = QtWidgets.QLineEdit()
                        valueObject.setText(value)

                        #Create path button
                        button = qtCore.pathButton()
                        button.mode = "AnyFile"
                        button.pathField = valueObject
                        button.setMaximumHeight(18)
                        button.setMinimumHeight(18)
                        valueObjects.append(button)

                        # Add connection
                        button.clicked.connect(button.add_path)
                    elif "path" in key or "dir" in key:
                        valueObject = QtWidgets.QLineEdit()
                        valueObject.setText(value)

                        # Create path button
                        button = qtCore.pathButton()
                        button.pathField = valueObject
                        button.setMaximumHeight(18)
                        button.setMinimumHeight(18)
                        valueObjects.append(button)

                        # Add connection
                        button.clicked.connect(button.add_path)
                    else:
                        valueObject = QtWidgets.QLineEdit()
                        valueObject.setText(value)


                elif type(value) == bool:
                    valueObject = QtWidgets.QCheckBox()

                    # Set value
                    if value == True:
                        valueObject.setChecked(True)
                elif type(value) == tuple or type(value) == list:
                    # Extra validation to check the type of the list
                    print len(value)
                    if len(value) == 3:
                        # Create Vector widget
                        print "This is a vector input"
                        valueObject = qtCore.vectorInput(widget=self)
                        valueObject.set_values(value[0], value[1], value[2])
                    elif len(value) >= 4:
                        # Create text input for list
                        valueObject = qtCore.vectorInput(widget=self)
                        valueObject.set_values(value[0], value[1], value[2])
                    else:
                        valueObject = qtCore.valueButton()
                        valueObject.multiple = True
                        valueObject.set_text("Object list")
                        # Create clicked method to update with the selection
                        valueObject.clicked.connect(valueObject.add_value)
                        valueObject.value = value
                elif type(value) == int:
                    valueObject = QtWidgets.QSpinBox()
                    valueObject.setValue(value)
                    valueObject.setMaximum(1000000000)
                elif type(value) == float:
                    valueObject = QtWidgets.QDoubleSpinBox()
                    valueObject.setValue(value)
                else:
                    valueObject = qtCore.valueButton()
                    valueObject.set_text("Single object")
                    # Create clicked method to update with the selection
                    valueObject.clicked.connect(valueObject.add_value)
                    valueObject.value = value

                # Set objectname from plug name
                valueObject.setObjectName(key)

                valueObjects.append(valueObject)
                for item in valueObjects[::-1]:
                    layout.addWidget(item)

                print "FROM:", last_tab_object
                print "TO:", valueObjects[0]
                self.setTabOrder(last_tab_object, valueObjects[0])
                last_tab_object = valueObjects[0]

                # Add to layout
                attributeLayout.addLayout(layout)

                # Set data for required or not
                valueObject.setProperty("required", required)

                # Feed label as property
                valueObject.setProperty("label", textLabel)
                valueObject.setObjectName(key)

                # Add to global object-list
                self.arguments.append(valueObject)

                # Add separator
                #line = qtCore.QHLine()
                #line.set_style("Plane")
                #attributeLayout.addWidget(line)

                self.attribute_objects.append(valueObject)

            # Add spacer in the end
            verticalSpacer = QtWidgets.QSpacerItem(20, 1000, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
            attributeLayout.addItem(verticalSpacer)


            # Add text with info for requirements
            if extraInfo["required"] != None:
                textLabel = QtWidgets.QLabel("* This argument is required for this function to run")
                textLabel.setStyleSheet("color: rgb(250,250,250,100)")
                attributeLayout.addWidget(textLabel)

        # Set focus
        print "SET FOCUS:", self.attribute_objects[0]
        self.attribute_objects[0].setFocus()

    def get_functions(self):
        # Define old selection
        if self.ui.functionList.count() >= 1:
            currentItem = self.ui.functionList.currentItem()
            card = currentItem.data(109)
            functionName = card.getTitle()
            oldSelection = functionName
        else:
            oldSelection = None

        # Block signals and clear layout
        self.ui.functionList.blockSignals(True)
        self.ui.functionList.setUpdatesEnabled(False)

        self.ui.functionList.clear()

        # Get proper functions list
        functionList = []
        for functionName in dir(mayaCore):
            # Define function
            function = getattr(mayaCore, functionName)
            # Check path
            try:
                path = inspect.getfile(function)
            except:
                path = None

            if path != None:
                if "mayaCore" in path:
                    if "pyc" not in path:
                        if callable(function):
                            functionList.append(function)

        # Sort functions by module
        sortedFunctionList = sorted(functionList, key=lambda function: inspect.getmodule(function).__file__.split(os.path.sep)[-1].split('.')[0])

        # Get functions
        currentModule = ""
        currentHeader = None

        # Add to the UI
        for function in sortedFunctionList:
            # Get module and create header
            module = inspect.getmodule(function)
            try:
                moduleName = module.__file__.split(os.path.sep)[-1].split('.')[0]
            except:
                moduleName = currentModule
            if moduleName != currentModule:
                currentModule = moduleName
                # Create header
                header = qtCore.widgets.create_header(title=moduleName, layout=self.ui.functionList)
            # Get info if exsits
            if function.__doc__ != None:
                docInfo = function.__doc__
            else:
                docInfo = "No info"


            # Create card
            item = qtCore.widgets.create_simple_card(title=function.__name__, height=20,layout=self.ui.functionList, info=docInfo)
            # Set data for header
            item.setData(100, moduleName)


        self.ui.functionList.setCurrentRow(1)


        # Enable signals again
        self.ui.functionList.blockSignals(False)
        self.ui.functionList.setUpdatesEnabled(True)

        # Set back text if it was there before
        if oldSelection != None:
            for number in range(self.ui.functionList.count()):
                item = self.ui.functionList.item(number)
                try:
                    if item.data(109).getTitle() == oldSelection:
                        self.ui.functionList.setCurrentRow(number)
                except:
                    pass

        return functionName

    def get_arguments(self):
        self.functionDictionary = []
        for functionName in dir(mayaCore):
            # Define function
            function = getattr(mayaCore, functionName)
            # Check if a path is accesable, if so it should be valid
            try:
                path = inspect.getfile(function)
            except:
                path = None

            if path != None:
                if "mayaCore" in path:
                    if "pyc" not in path:
                        if callable(function):
                            #Reload module
                            module = inspect.getmodule(function)

                            try: reload(module)
                            except Exception, errorMessage:
                                print "ERROR: Problem loading", module
                                print errorMessage

                            # Get specs
                            spec = inspect.getargspec(function)

                            # Crate base dictionary
                            defaults = dict(zip(spec.args[::-1], (spec.defaults or ())[::-1]))

                            # Empty values
                            if len(defaults) == 0:
                                # Set default value as None for things with no values
                                defaults = dict(zip(spec.args, [None for value in spec.args]))
                            else:
                                emptyValyes = dict(zip(spec.args[:-len(defaults)], [None for value in spec.args[:-len(defaults)]]))
                                # Put the list together
                                defaults.update(emptyValyes)

                            # Add to list
                            output = [function, function.__name__, function.__doc__, defaults]
                            self.functionDictionary.append(output)
        return self.functionDictionary


