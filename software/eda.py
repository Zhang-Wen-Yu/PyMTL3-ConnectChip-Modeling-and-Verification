# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eda.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1211, 785)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Connect_Configure_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Connect_Configure_groupBox.setObjectName("Connect_Configure_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Connect_Configure_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Connect_button = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Connect_button.setObjectName("Connect_button")
        self.gridLayout_4.addWidget(self.Connect_button, 2, 1, 1, 1)
        self.Master_Button_Brower = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Master_Button_Brower.setObjectName("Master_Button_Brower")
        self.gridLayout_4.addWidget(self.Master_Button_Brower, 0, 2, 1, 1)
        self.Update_Button = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Update_Button.setObjectName("Update_Button")
        self.gridLayout_4.addWidget(self.Update_Button, 2, 2, 1, 1)
        self.Master_File_label = QtWidgets.QLabel(self.Connect_Configure_groupBox)
        self.Master_File_label.setObjectName("Master_File_label")
        self.gridLayout_4.addWidget(self.Master_File_label, 0, 0, 1, 1)
        self.Master_File_Line_Edit = QtWidgets.QLineEdit(self.Connect_Configure_groupBox)
        self.Master_File_Line_Edit.setObjectName("Master_File_Line_Edit")
        self.gridLayout_4.addWidget(self.Master_File_Line_Edit, 0, 1, 1, 1)
        self.Slave_File_Line_Edit = QtWidgets.QLineEdit(self.Connect_Configure_groupBox)
        self.Slave_File_Line_Edit.setObjectName("Slave_File_Line_Edit")
        self.gridLayout_4.addWidget(self.Slave_File_Line_Edit, 1, 1, 1, 1)
        self.Slave_Button = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Slave_Button.setObjectName("Slave_Button")
        self.gridLayout_4.addWidget(self.Slave_Button, 1, 2, 1, 1)
        self.Slave_File_label = QtWidgets.QLabel(self.Connect_Configure_groupBox)
        self.Slave_File_label.setObjectName("Slave_File_label")
        self.gridLayout_4.addWidget(self.Slave_File_label, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.Connect_Configure_groupBox, 3, 1, 1, 1)
        self.Mode_Selection_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.Mode_Selection_groupbox.setObjectName("Mode_Selection_groupbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Mode_Selection_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Apply_button_inmode = QtWidgets.QPushButton(self.Mode_Selection_groupbox)
        self.Apply_button_inmode.setObjectName("Apply_button_inmode")
        self.gridLayout_3.addWidget(self.Apply_button_inmode, 1, 2, 1, 1)
        self.Mode_select_comboBox = QtWidgets.QComboBox(self.Mode_Selection_groupbox)
        self.Mode_select_comboBox.setObjectName("Mode_select_comboBox")
        self.gridLayout_3.addWidget(self.Mode_select_comboBox, 1, 1, 1, 1)
        self.Current_Mode_label = QtWidgets.QLabel(self.Mode_Selection_groupbox)
        self.Current_Mode_label.setObjectName("Current_Mode_label")
        self.gridLayout_3.addWidget(self.Current_Mode_label, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.Mode_Selection_groupbox, 4, 1, 1, 1)
        self.json_file_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.json_file_groupbox.setObjectName("json_file_groupbox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.json_file_groupbox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.json_name_line_edit = QtWidgets.QLineEdit(self.json_file_groupbox)
        self.json_name_line_edit.setObjectName("json_name_line_edit")
        self.gridLayout_5.addWidget(self.json_name_line_edit, 1, 1, 1, 1)
        self.json_file_label = QtWidgets.QLabel(self.json_file_groupbox)
        self.json_file_label.setObjectName("json_file_label")
        self.gridLayout_5.addWidget(self.json_file_label, 0, 0, 1, 1)
        self.json_name_label = QtWidgets.QLabel(self.json_file_groupbox)
        self.json_name_label.setObjectName("json_name_label")
        self.gridLayout_5.addWidget(self.json_name_label, 1, 0, 1, 1)
        self.json_file_line_edit = QtWidgets.QLineEdit(self.json_file_groupbox)
        self.json_file_line_edit.setObjectName("json_file_line_edit")
        self.gridLayout_5.addWidget(self.json_file_line_edit, 0, 1, 1, 1)
        self.Apply_Button_injson = QtWidgets.QPushButton(self.json_file_groupbox)
        self.Apply_Button_injson.setObjectName("Apply_Button_injson")
        self.gridLayout_5.addWidget(self.Apply_Button_injson, 1, 2, 1, 1)
        self.brower_button = QtWidgets.QPushButton(self.json_file_groupbox)
        self.brower_button.setObjectName("brower_button")
        self.gridLayout_5.addWidget(self.brower_button, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.json_file_groupbox, 1, 1, 1, 1)
        self.Message_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Message_groupBox.setObjectName("Message_groupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.Message_groupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.Message_Text_Edit = QtWidgets.QTextBrowser(self.Message_groupBox)
        self.Message_Text_Edit.setObjectName("Message_Text_Edit")
        self.gridLayout_6.addWidget(self.Message_Text_Edit, 0, 0, 1, 1)
        self.Clear_Button = QtWidgets.QPushButton(self.Message_groupBox)
        self.Clear_Button.setObjectName("Clear_Button")
        self.gridLayout_6.addWidget(self.Clear_Button, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.Message_groupBox, 5, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 611, 671))
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 5, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1211, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Connect_Configure_groupBox.setTitle(_translate("MainWindow", "Connect Configure"))
        self.Connect_button.setText(_translate("MainWindow", "Connect"))
        self.Master_Button_Brower.setText(_translate("MainWindow", "Browser"))
        self.Update_Button.setText(_translate("MainWindow", "Update"))
        self.Master_File_label.setText(_translate("MainWindow", "Master File："))
        self.Slave_Button.setText(_translate("MainWindow", "Browser"))
        self.Slave_File_label.setText(_translate("MainWindow", "Slave  File："))
        self.Mode_Selection_groupbox.setTitle(_translate("MainWindow", "Mode Selection"))
        self.Apply_button_inmode.setText(_translate("MainWindow", "Apply"))
        self.Current_Mode_label.setText(_translate("MainWindow", "Current Mode："))
        self.json_file_groupbox.setTitle(_translate("MainWindow", "Json File"))
        self.json_file_label.setText(_translate("MainWindow", "Json File："))
        self.json_name_label.setText(_translate("MainWindow", "Json name："))
        self.Apply_Button_injson.setText(_translate("MainWindow", "Apply"))
        self.brower_button.setText(_translate("MainWindow", "Browser"))
        self.Message_groupBox.setTitle(_translate("MainWindow", "Message"))
        self.Clear_Button.setText(_translate("MainWindow", "Clear"))
        self.groupBox.setTitle(_translate("MainWindow", "                         Hardware Connect Window                           "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())