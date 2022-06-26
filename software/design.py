from crc_eda import *


class crc_tools(Ui_MainWindow):

    def logic(self):

        # sign
        self.Browser_in_json = 0
        self.apply_json = 0
        self.master_browser = 0
        self.master_click = 0
        self.slave_browser = 0
        self.slave_click = 0

        # button_click
        self.Slave_Button_brower.clicked.connect(self.Slave_Button)
        self.Master_Button_Brower.clicked.connect(self.Master_Button)
        self.Clear_Button.clicked.connect(self.clear_button)
        self.Apply_Button_injson.clicked.connect(self.apply_in_json_file)
        self.brower_button.clicked.connect(self.Button_in_Json_File)

    def Button_in_Json_File(self):
        m, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "",
                                                      "D:/Desktop/pModel-20220530/Config", "json (*.json)")
        if ''.join(m) != '':
            self.json_file_line_edit.setText(''.join(m))
            self.json_name_line_edit.setText(m[0])
            self.Message_Text_Edit.append(str(timestamp) + ': ' + 'Browser json file successful')
            self.Browser_in_json = 1
        else:
            self.Browser_in_json = 0

    def Master_Button(self):
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "",
                                                       "D:/Desktop/pModel-20220530/Module")
        if m != '':
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
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "",
                                                       "D:/Desktop/pModel-20220530/Module")

        if m != '':
            self.slave_click = 1
        else:
            self.slave_click = 0

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

