# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eda.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
curr_time = datetime.datetime.now()
timestamp = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):


        # sign
        self.Browser_in_json = 0
        self.apply_json = 0
        self.master_browser = 0
        self.master_click = 0
        self.slave_browser = 0
        self.slave_click = 0



        MainWindow.setObjectName("CRC")
        MainWindow.resize(1302, 849)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.Connect_Configure_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Connect_Configure_groupBox.setGeometry(QtCore.QRect(740, 120, 531, 141))
        self.Connect_Configure_groupBox.setObjectName("Connect_Configure_groupBox")
        self.Master_File_label = QtWidgets.QLabel(self.Connect_Configure_groupBox)
        self.Master_File_label.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.Master_File_label.setObjectName("Master_File_label")
        self.Slave_File_label = QtWidgets.QLabel(self.Connect_Configure_groupBox)
        self.Slave_File_label.setGeometry(QtCore.QRect(10, 70, 101, 16))
        self.Slave_File_label.setObjectName("Slave_File_label")

        # slave button
        self.Slave_Button_brower = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Slave_Button_brower.setGeometry(QtCore.QRect(420, 65, 93, 28))
        self.Slave_Button_brower.setObjectName("Slave_Button_brower")
        self.Slave_Button_brower.clicked.connect(self.Slave_Button)

        # master button
        self.Master_Button_Brower = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Master_Button_Brower.setGeometry(QtCore.QRect(420, 25, 93, 28))
        self.Master_Button_Brower.setObjectName("Master_Button_Brower")
        self.Master_Button_Brower.clicked.connect(self.Master_Button)


        self.Connect_button = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Connect_button.setGeometry(QtCore.QRect(110, 100, 301, 28))
        self.Connect_button.setObjectName("Connect_button")
        self.Update_Button = QtWidgets.QPushButton(self.Connect_Configure_groupBox)
        self.Update_Button.setGeometry(QtCore.QRect(420, 100, 93, 28))
        self.Update_Button.setObjectName("Update_Button")

        self.Master_File_Line_Edit = QtWidgets.QLineEdit(self.Connect_Configure_groupBox)
        self.Master_File_Line_Edit.setGeometry(QtCore.QRect(110, 30, 301, 21))
        self.Master_File_Line_Edit.setObjectName("Master_File_Line_Edit")

        self.Slave_File_Line_Edit = QtWidgets.QLineEdit(self.Connect_Configure_groupBox)
        self.Slave_File_Line_Edit.setGeometry(QtCore.QRect(110, 70, 301, 21))
        self.Slave_File_Line_Edit.setObjectName("Slave_File_Line_Edit")

        # Message window
        self.Message_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Message_groupBox.setGeometry(QtCore.QRect(740, 370, 531, 411))
        self.Message_groupBox.setObjectName("Message_groupBox")
        self.Message_Text_Edit = QtWidgets.QTextBrowser(self.Message_groupBox)
        self.Message_Text_Edit.setGeometry(QtCore.QRect(10, 20, 511, 351))
        self.Message_Text_Edit.setObjectName("Message_Text_Edit")


        # clear button
        self.Clear_Button = QtWidgets.QPushButton(self.Message_groupBox)
        self.Clear_Button.setGeometry(QtCore.QRect(10, 380, 511, 28))
        self.Clear_Button.setObjectName("Clear_Button")
        self.Clear_Button.clicked.connect(self.clear_button)


        self.json_file_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.json_file_groupbox.setGeometry(QtCore.QRect(740, 10, 531, 101))
        self.json_file_groupbox.setObjectName("json_file_groupbox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.json_file_groupbox)
        self.gridLayout_5.setObjectName("gridLayout_5")


        # json name line edit
        self.json_name_line_edit = QtWidgets.QLineEdit(self.json_file_groupbox)
        self.json_name_line_edit.setGeometry(QtCore.QRect(100, 70, 301, 21))
        self.json_name_line_edit.setObjectName("json_name_line_edit")
        self.json_name_line_edit.setReadOnly(True)
        self.gridLayout_5.addWidget(self.json_name_line_edit, 1, 1, 1, 1)


        # apply button in json file
        self.Apply_Button_injson = QtWidgets.QPushButton(self.json_file_groupbox)
        self.Apply_Button_injson.setGeometry(QtCore.QRect(420, 65, 93, 28))
        self.Apply_Button_injson.setObjectName("Apply_Button_injson")
        self.gridLayout_5.addWidget(self.Apply_Button_injson, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.json_file_groupbox, 0, 1, 1, 1)
        self.Apply_Button_injson.clicked.connect(self.apply_in_json_file)
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Connect_Configure_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")

        # Brower Button in JSON FILE
        self.brower_button = QtWidgets.QPushButton(self.json_file_groupbox)
        self.brower_button.setGeometry(QtCore.QRect(420, 25, 93, 28))
        self.brower_button.setObjectName("brower_button")
        self.brower_button.clicked.connect(self.Button_in_Json_File)
        self.gridLayout_5.addWidget(self.brower_button, 0, 2, 1, 1)



        self.json_file_label = QtWidgets.QLabel(self.json_file_groupbox)
        self.json_file_label.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.json_file_label.setObjectName("json_file_label")
        self.gridLayout_5.addWidget(self.json_file_label, 0, 0, 1, 1)


        self.json_name_label = QtWidgets.QLabel(self.json_file_groupbox)
        self.json_name_label.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.json_name_label.setObjectName("json_name_label")
        self.gridLayout_5.addWidget(self.json_name_label, 1, 0, 1, 1)


        # json file line edit
        self.json_file_line_edit = QtWidgets.QLineEdit(self.json_file_groupbox)
        self.json_file_line_edit.setGeometry(QtCore.QRect(100, 30, 301, 21))
        self.json_file_line_edit.setObjectName("json_file_line_edit")
        self.json_file_line_edit.setReadOnly(True)
        self.gridLayout_5.addWidget(self.json_file_line_edit, 0, 1, 1, 1)


        self.Mode_Selection_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.Mode_Selection_groupbox.setGeometry(QtCore.QRect(740, 270, 531, 91))
        self.Mode_Selection_groupbox.setObjectName("Mode_Selection_groupbox")

        self.Current_Mode_label = QtWidgets.QLabel(self.Mode_Selection_groupbox)
        self.Current_Mode_label.setGeometry(QtCore.QRect(90, 50, 111, 16))
        self.Current_Mode_label.setObjectName("Current_Mode_label")

        self.Apply_button_inmode = QtWidgets.QPushButton(self.Mode_Selection_groupbox)
        self.Apply_button_inmode.setGeometry(QtCore.QRect(380, 45, 141, 28))
        self.Apply_button_inmode.setObjectName("Apply_button_inmode")

        self.Mode_select_comboBox = QtWidgets.QComboBox(self.Mode_Selection_groupbox)
        self.Mode_select_comboBox.setGeometry(QtCore.QRect(190, 50, 181, 21))
        self.Mode_select_comboBox.setObjectName("Mode_select_comboBox")

        self.hardware_show = QtWidgets.QTextBrowser(self.centralwidget)
        self.hardware_show.setGeometry(QtCore.QRect(10, 10, 721, 771))
        self.hardware_show.setObjectName("hardware_show")
        self.gridLayout_2.addWidget(self.hardware_show, 0, 0, 4, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1302, 26))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.gridLayout_4.addWidget(self.Master_File_label, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.Master_File_Line_Edit, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.Master_Button_Brower, 0, 2, 1, 1)
        self.gridLayout_4.addWidget(self.Slave_File_label, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.Slave_File_Line_Edit, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.Slave_Button_brower, 1, 2, 1, 1)
        self.gridLayout_4.addWidget(self.Connect_button, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.Update_Button, 2, 2, 1, 1)
        self.gridLayout_2.addWidget(self.Connect_Configure_groupBox, 1, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Mode_Selection_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.addWidget(self.Current_Mode_label, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.Mode_select_comboBox, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.Apply_button_inmode, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.Mode_Selection_groupbox, 2, 1, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.Message_groupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.addWidget(self.Message_Text_Edit, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.Clear_Button, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.Message_groupBox, 3, 1, 1, 1)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CRC Simulation Backend Tools v1.0"))
        self.Connect_Configure_groupBox.setTitle(_translate("MainWindow", "Connect Configure"))
        self.Master_File_label.setText(_translate("MainWindow", "Master File："))
        self.Slave_File_label.setText(_translate("MainWindow", "Slave  File："))
        self.Slave_Button_brower.setText(_translate("MainWindow", "Browser"))
        self.Master_Button_Brower.setText(_translate("MainWindow", "Browser"))
        self.Connect_button.setText(_translate("MainWindow", "Connect"))
        self.Update_Button.setText(_translate("MainWindow", "Update"))
        self.Message_groupBox.setTitle(_translate("MainWindow", "Message"))
        self.Clear_Button.setText(_translate("MainWindow", "Clear"))
        self.json_file_groupbox.setTitle(_translate("MainWindow", "Json File"))
        self.Apply_Button_injson.setText(_translate("MainWindow", "Apply"))
        self.brower_button.setText(_translate("MainWindow", "Browser"))
        self.json_file_label.setText(_translate("MainWindow", "Json File："))
        self.json_name_label.setText(_translate("MainWindow", "Json name："))
        self.Mode_Selection_groupbox.setTitle(_translate("MainWindow", "Mode Selection"))
        self.Current_Mode_label.setText(_translate("MainWindow", "Current Mode："))
        self.Apply_button_inmode.setText(_translate("MainWindow", "Apply"))


    def Button_in_Json_File(self):
        m,_= QtWidgets.QFileDialog.getOpenFileNames(None, "",
                                                   "D:/Desktop/pModel-20220530/Config","json (*.json)")
        if ''.join(m) !='':
         self.json_file_line_edit.setText(''.join(m))
         self.json_name_line_edit.setText(m[0])
         self.Message_Text_Edit.append(str(timestamp) + ': ' + 'Browser json file successful')
         self.Browser_in_json = 1
        else:
         self.Browser_in_json = 0

    def Master_Button(self):
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "",
                                                      "D:/Desktop/pModel-20220530/Module" )

        if m !='':
            self.master_click = 1
        else:
            self.master_click = 0

        if self.apply_json == 1:
         if m != '':
            self.Master_File_Line_Edit.setText(m)
            self.Message_Text_Edit.append(str(timestamp) + ': ' + 'Browser Master file successful')
            self.master_browser = 1
         else:
            self.master_browser = 0

        else:
            if self.master_click == 1:
                self.Message_Text_Edit.append(str(timestamp) + ': ' + "you don't load json file")

    def Slave_Button(self):
        m= QtWidgets.QFileDialog.getExistingDirectory(None, "",
                                                  "D:/Desktop/pModel-20220530/Module")

        if m != '':
            self.slave_click = 1
        else:
            self.slave_click =0

        if self.apply_json == 1:
         if m != '':
          self.Slave_File_Line_Edit.setText(m)
          self.Message_Text_Edit.append(str(timestamp) + ': ' + 'Browser Slave file successful')
          self.slave_browser = 1
         else:
            self.slave_browser = 0
        else:
            if self.slave_click == 1:
              self.Message_Text_Edit.append(str(timestamp) + ': ' + "you don't load json file")


    def apply_in_json_file(self):
        if self.Browser_in_json == 1:
            self.Message_Text_Edit.append(str(timestamp) + ': ' + 'Apply json file successful')
            self.Browser_in_json = 0
            self.apply_json = 1
        else:
            self.Message_Text_Edit.append(str(timestamp) + ': ' + 'you not load a json file')
            self.apply_json = 0



    def clear_button(self):
        self.Message_Text_Edit.clear()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())