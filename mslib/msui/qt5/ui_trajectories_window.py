# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_trajectories_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TrajectoriesWindow(object):
    def setupUi(self, TrajectoriesWindow):
        TrajectoriesWindow.setObjectName("TrajectoriesWindow")
        TrajectoriesWindow.resize(732, 725)
        self.centralwidget = QtWidgets.QWidget(TrajectoriesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabGUI = QtWidgets.QTabWidget(self.centralwidget)
        self.tabGUI.setEnabled(True)
        self.tabGUI.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabGUI.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabGUI.setObjectName("tabGUI")
        self.tabData = QtWidgets.QWidget()
        self.tabData.setObjectName("tabData")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabData)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.tabData)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self._5 = QtWidgets.QVBoxLayout(self.groupBox)
        self._5.setObjectName("_5")
        self._6 = QtWidgets.QHBoxLayout()
        self._6.setObjectName("_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self._6.addWidget(self.label_4)
        self.leSelectionQuery = QtWidgets.QLineEdit(self.groupBox)
        self.leSelectionQuery.setObjectName("leSelectionQuery")
        self._6.addWidget(self.leSelectionQuery)
        self.cbSelectElements = QtWidgets.QComboBox(self.groupBox)
        self.cbSelectElements.setObjectName("cbSelectElements")
        self.cbSelectElements.addItem("")
        self.cbSelectElements.addItem("")
        self._6.addWidget(self.cbSelectElements)
        self.btSelectMapElements = QtWidgets.QPushButton(self.groupBox)
        self.btSelectMapElements.setObjectName("btSelectMapElements")
        self._6.addWidget(self.btSelectMapElements)
        self._5.addLayout(self._6)
        self.tvVisibleElements = QtWidgets.QTreeView(self.groupBox)
        self.tvVisibleElements.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tvVisibleElements.setSortingEnabled(False)
        self.tvVisibleElements.setObjectName("tvVisibleElements")
        self._5.addWidget(self.tvVisibleElements)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_7 = QtWidgets.QGroupBox(self.tabData)
        self.groupBox_7.setFlat(True)
        self.groupBox_7.setObjectName("groupBox_7")
        self._7 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self._7.setObjectName("_7")
        self._8 = QtWidgets.QVBoxLayout()
        self._8.setObjectName("_8")
        self._9 = QtWidgets.QHBoxLayout()
        self._9.setObjectName("_9")
        self.label = QtWidgets.QLabel(self.groupBox_7)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setObjectName("label")
        self._9.addWidget(self.label)
        self.cbColour = QtWidgets.QComboBox(self.groupBox_7)
        self.cbColour.setMinimumSize(QtCore.QSize(80, 0))
        self.cbColour.setObjectName("cbColour")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self.cbColour.addItem("")
        self._9.addWidget(self.cbColour)
        self.btColour = QtWidgets.QPushButton(self.groupBox_7)
        self.btColour.setMinimumSize(QtCore.QSize(60, 0))
        self.btColour.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btColour.setObjectName("btColour")
        self._9.addWidget(self.btColour)
        self._8.addLayout(self._9)
        self._10 = QtWidgets.QHBoxLayout()
        self._10.setObjectName("_10")
        self.label_2 = QtWidgets.QLabel(self.groupBox_7)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_2.setObjectName("label_2")
        self._10.addWidget(self.label_2)
        self.cbLineStyle = QtWidgets.QComboBox(self.groupBox_7)
        self.cbLineStyle.setMinimumSize(QtCore.QSize(80, 0))
        self.cbLineStyle.setObjectName("cbLineStyle")
        self.cbLineStyle.addItem("")
        self.cbLineStyle.addItem("")
        self.cbLineStyle.addItem("")
        self.cbLineStyle.addItem("")
        self.cbLineStyle.addItem("")
        self._10.addWidget(self.cbLineStyle)
        self.btLineStyle = QtWidgets.QPushButton(self.groupBox_7)
        self.btLineStyle.setMinimumSize(QtCore.QSize(60, 0))
        self.btLineStyle.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btLineStyle.setObjectName("btLineStyle")
        self._10.addWidget(self.btLineStyle)
        self._8.addLayout(self._10)
        self._11 = QtWidgets.QHBoxLayout()
        self._11.setObjectName("_11")
        self.label_3 = QtWidgets.QLabel(self.groupBox_7)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_3.setObjectName("label_3")
        self._11.addWidget(self.label_3)
        self.sbLineWidth = QtWidgets.QSpinBox(self.groupBox_7)
        self.sbLineWidth.setMinimumSize(QtCore.QSize(80, 0))
        self.sbLineWidth.setMinimum(1)
        self.sbLineWidth.setObjectName("sbLineWidth")
        self._11.addWidget(self.sbLineWidth)
        self.btLineWidth = QtWidgets.QPushButton(self.groupBox_7)
        self.btLineWidth.setMinimumSize(QtCore.QSize(60, 0))
        self.btLineWidth.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btLineWidth.setObjectName("btLineWidth")
        self._11.addWidget(self.btLineWidth)
        self._8.addLayout(self._11)
        self._7.addLayout(self._8)
        self.line_3 = QtWidgets.QFrame(self.groupBox_7)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self._7.addWidget(self.line_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self._13 = QtWidgets.QHBoxLayout()
        self._13.setObjectName("_13")
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setObjectName("label_5")
        self._13.addWidget(self.label_5)
        self.teTimeMarker = QtWidgets.QTimeEdit(self.groupBox_7)
        self.teTimeMarker.setObjectName("teTimeMarker")
        self._13.addWidget(self.teTimeMarker)
        self.btTimeMarker = QtWidgets.QPushButton(self.groupBox_7)
        self.btTimeMarker.setMinimumSize(QtCore.QSize(60, 0))
        self.btTimeMarker.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btTimeMarker.setObjectName("btTimeMarker")
        self._13.addWidget(self.btTimeMarker)
        self.verticalLayout_2.addLayout(self._13)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.groupBox_7)
        self.label_6.setMinimumSize(QtCore.QSize(110, 0))
        self.label_6.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.cbPlotInView = QtWidgets.QComboBox(self.groupBox_7)
        self.cbPlotInView.setMinimumSize(QtCore.QSize(150, 0))
        self.cbPlotInView.setObjectName("cbPlotInView")
        self.cbPlotInView.addItem("")
        self.horizontalLayout.addWidget(self.cbPlotInView)
        self.btPlotInView = QtWidgets.QPushButton(self.groupBox_7)
        self.btPlotInView.setMinimumSize(QtCore.QSize(60, 0))
        self.btPlotInView.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btPlotInView.setObjectName("btPlotInView")
        self.horizontalLayout.addWidget(self.btPlotInView)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_7)
        self.label_7.setMinimumSize(QtCore.QSize(110, 0))
        self.label_7.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.cbRemoveFromView = QtWidgets.QComboBox(self.groupBox_7)
        self.cbRemoveFromView.setMinimumSize(QtCore.QSize(150, 0))
        self.cbRemoveFromView.setObjectName("cbRemoveFromView")
        self.cbRemoveFromView.addItem("")
        self.horizontalLayout_2.addWidget(self.cbRemoveFromView)
        self.btRemoveFromView = QtWidgets.QPushButton(self.groupBox_7)
        self.btRemoveFromView.setMinimumSize(QtCore.QSize(60, 0))
        self.btRemoveFromView.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btRemoveFromView.setObjectName("btRemoveFromView")
        self.horizontalLayout_2.addWidget(self.btRemoveFromView)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self._7.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addWidget(self.groupBox_7)
        self.tabGUI.addTab(self.tabData, "")
        self.verticalLayout.addWidget(self.tabGUI)
        TrajectoriesWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TrajectoriesWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 732, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        TrajectoriesWindow.setMenuBar(self.menubar)
        self.actionOpenTrajectories = QtWidgets.QAction(TrajectoriesWindow)
        self.actionOpenTrajectories.setObjectName("actionOpenTrajectories")
        self.actionOpenFlightTrack = QtWidgets.QAction(TrajectoriesWindow)
        self.actionOpenFlightTrack.setObjectName("actionOpenFlightTrack")
        self.action_Quit = QtWidgets.QAction(TrajectoriesWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.actionCloseElement = QtWidgets.QAction(TrajectoriesWindow)
        self.actionCloseElement.setObjectName("actionCloseElement")
        self.menu_File.addAction(self.actionOpenTrajectories)
        self.menu_File.addAction(self.actionOpenFlightTrack)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(TrajectoriesWindow)
        self.tabGUI.setCurrentIndex(0)
        self.cbSelectElements.setCurrentIndex(0)
        self.action_Quit.triggered.connect(TrajectoriesWindow.close)
        QtCore.QMetaObject.connectSlotsByName(TrajectoriesWindow)

    def retranslateUi(self, TrajectoriesWindow):
        _translate = QtCore.QCoreApplication.translate
        TrajectoriesWindow.setWindowTitle(_translate("TrajectoriesWindow", "Trajectories - Mission Support System"))
        self.groupBox.setTitle(_translate("TrajectoriesWindow", "Open trajectory items:"))
        self.label_4.setText(_translate("TrajectoriesWindow", "Select:"))
        self.leSelectionQuery.setToolTip(_translate("TrajectoriesWindow", "Enter selection criteria here. Available variables are %lat, %lon, %pres, \n"
"and %meta(\"NAME\"), where NAME has to be the name of a matatag that appears in the data. \n"
"For example, type \'%lat >= 45.\' will select all elements with a start point latitude larger \n"
"equal to 45 degrees after you click the button on the left. To select all trajectories with a \n"
"start latitude larger than 45 degrees at flight level 320, type \'%lat > 45. and %meta(\"flightlevel\") == 320\'."))
        self.cbSelectElements.setItemText(0, _translate("TrajectoriesWindow", "from all items"))
        self.cbSelectElements.setItemText(1, _translate("TrajectoriesWindow", "from children of current node"))
        self.btSelectMapElements.setToolTip(_translate("TrajectoriesWindow", "Select all items listed below that match the criteria given on the right."))
        self.btSelectMapElements.setText(_translate("TrajectoriesWindow", "&go!"))
        self.groupBox_7.setTitle(_translate("TrajectoriesWindow", "Modify selected items:"))
        self.label.setText(_translate("TrajectoriesWindow", "Colour:"))
        self.cbColour.setItemText(0, _translate("TrajectoriesWindow", "None"))
        self.cbColour.setItemText(1, _translate("TrajectoriesWindow", "blue"))
        self.cbColour.setItemText(2, _translate("TrajectoriesWindow", "green"))
        self.cbColour.setItemText(3, _translate("TrajectoriesWindow", "red"))
        self.cbColour.setItemText(4, _translate("TrajectoriesWindow", "cyan"))
        self.cbColour.setItemText(5, _translate("TrajectoriesWindow", "magenta"))
        self.cbColour.setItemText(6, _translate("TrajectoriesWindow", "yellow"))
        self.cbColour.setItemText(7, _translate("TrajectoriesWindow", "black"))
        self.cbColour.setItemText(8, _translate("TrajectoriesWindow", "white"))
        self.btColour.setToolTip(_translate("TrajectoriesWindow", "Set the colour of the selected items."))
        self.btColour.setText(_translate("TrajectoriesWindow", "apply"))
        self.label_2.setText(_translate("TrajectoriesWindow", "Line Style:"))
        self.cbLineStyle.setItemText(0, _translate("TrajectoriesWindow", "None"))
        self.cbLineStyle.setItemText(1, _translate("TrajectoriesWindow", "-"))
        self.cbLineStyle.setItemText(2, _translate("TrajectoriesWindow", "--"))
        self.cbLineStyle.setItemText(3, _translate("TrajectoriesWindow", "-."))
        self.cbLineStyle.setItemText(4, _translate("TrajectoriesWindow", ":"))
        self.btLineStyle.setToolTip(_translate("TrajectoriesWindow", "Set the line style of the selected items."))
        self.btLineStyle.setText(_translate("TrajectoriesWindow", "apply"))
        self.label_3.setText(_translate("TrajectoriesWindow", "Line Width:"))
        self.btLineWidth.setToolTip(_translate("TrajectoriesWindow", "Set the line width of the selected items."))
        self.btLineWidth.setText(_translate("TrajectoriesWindow", "apply"))
        self.label_5.setText(_translate("TrajectoriesWindow", "Draw time markers (hh:mm):"))
        self.teTimeMarker.setDisplayFormat(_translate("TrajectoriesWindow", "hh:mm"))
        self.btTimeMarker.setToolTip(_translate("TrajectoriesWindow", "Draw time markers along the trajectories. These will be dots with the spacing given on the right (hh:mm)."))
        self.btTimeMarker.setText(_translate("TrajectoriesWindow", "apply"))
        self.label_6.setText(_translate("TrajectoriesWindow", "Plot in view:"))
        self.cbPlotInView.setItemText(0, _translate("TrajectoriesWindow", "None"))
        self.btPlotInView.setText(_translate("TrajectoriesWindow", "apply"))
        self.label_7.setText(_translate("TrajectoriesWindow", "Remove from view:"))
        self.cbRemoveFromView.setItemText(0, _translate("TrajectoriesWindow", "None"))
        self.btRemoveFromView.setText(_translate("TrajectoriesWindow", "apply"))
        self.tabGUI.setTabText(self.tabGUI.indexOf(self.tabData), _translate("TrajectoriesWindow", "Data"))
        self.menu_File.setTitle(_translate("TrajectoriesWindow", "&File"))
        self.actionOpenTrajectories.setText(_translate("TrajectoriesWindow", "&Open Trajectories..."))
        self.actionOpenTrajectories.setShortcut(_translate("TrajectoriesWindow", "Ctrl+O"))
        self.actionOpenFlightTrack.setText(_translate("TrajectoriesWindow", "Open &Flight Track..."))
        self.actionOpenFlightTrack.setShortcut(_translate("TrajectoriesWindow", "Ctrl+F"))
        self.action_Quit.setText(_translate("TrajectoriesWindow", "&Exit"))
        self.action_Quit.setShortcut(_translate("TrajectoriesWindow", "Ctrl+X"))
        self.actionCloseElement.setText(_translate("TrajectoriesWindow", "&Close Element..."))

