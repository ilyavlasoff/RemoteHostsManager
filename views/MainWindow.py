# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(472, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.catalogTreeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.catalogTreeWidget.setGeometry(QtCore.QRect(10, 170, 451, 401))
        self.catalogTreeWidget.setObjectName("catalogTreeWidget")
        self.catalogTreeWidget.headerItem().setText(0, "1")
        self.partitionsListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.partitionsListWidget.setGeometry(QtCore.QRect(10, 10, 451, 151))
        self.partitionsListWidget.setObjectName("partitionsListWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 472, 22))
        self.menubar.setObjectName("menubar")
        self.menuHosts = QtWidgets.QMenu(self.menubar)
        self.menuHosts.setObjectName("menuHosts")
        self.menuConnection = QtWidgets.QMenu(self.menubar)
        self.menuConnection.setObjectName("menuConnection")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHost_list = QtWidgets.QAction(MainWindow)
        self.actionHost_list.setObjectName("actionHost_list")
        self.actionSaved_hosts = QtWidgets.QAction(MainWindow)
        self.actionSaved_hosts.setObjectName("actionSaved_hosts")
        self.actionConnect_to = QtWidgets.QAction(MainWindow)
        self.actionConnect_to.setObjectName("actionConnect_to")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionConnection_properties = QtWidgets.QAction(MainWindow)
        self.actionConnection_properties.setObjectName("actionConnection_properties")
        self.menuHosts.addAction(self.actionHost_list)
        self.menuHosts.addAction(self.actionSaved_hosts)
        self.menuConnection.addAction(self.actionConnect_to)
        self.menuConnection.addAction(self.actionDisconnect)
        self.menuConnection.addAction(self.actionConnection_properties)
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuHosts.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Remote hosts disk management"))
        self.menuHosts.setTitle(_translate("MainWindow", "Hosts"))
        self.menuConnection.setTitle(_translate("MainWindow", "Connection"))
        self.actionHost_list.setText(_translate("MainWindow", "Add a host"))
        self.actionSaved_hosts.setText(_translate("MainWindow", "Saved hosts"))
        self.actionConnect_to.setText(_translate("MainWindow", "Connect to..."))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionConnection_properties.setText(_translate("MainWindow", "Connection properties"))
