from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as ms
from pathlib import Path
from expression_evaluation import begin_eval
from preset_management import begin, new_temp
from start_up import check_password

def relative_to_bg(path: str) -> Path:
        return BG_PATH / Path(path)
OUTPUT_PATH = Path(__file__).parent
BG_PATH = OUTPUT_PATH / Path("./backgrounds")

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(500, 654)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 500, 654))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(str(relative_to_bg("bg.jpg"))))
        self.bg.setObjectName("bg")
        self.hide = QtWidgets.QLabel(self.centralwidget)
        self.hide.setGeometry(QtCore.QRect(20, 600, 461, 31))
        self.hide.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.hide.setText("")
        self.hide.setObjectName("hide")
        self.pwd_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pwd_input.setGeometry(QtCore.QRect(247, 473, 231, 28))
        self.pwd_input.setStyleSheet("background-color: rgb(255, 131, 133);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.pwd_input.setText("")
        self.pwd_input.setFrame(False)
        self.pwd_input.setObjectName("pwd_input")
        self.pwd_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.submit = QtWidgets.QPushButton(self.centralwidget,clicked=lambda:self.login())
        self.submit.setGeometry(QtCore.QRect(185, 535, 135, 45))
        self.submit.setStyleSheet("background-color: rgb(255, 67, 70);\n"
"font: 20pt \"Franklin Gothic Demi Cond\";")
        self.submit.setAutoDefault(False)
        self.submit.setFlat(False)
        self.submit.setObjectName("submit")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "AlphaCalc"))
        self.submit.setText(_translate("LoginWindow", "Submit"))

    def login(self):
        QtCore.pyqtRemoveInputHook() 
        from calculator import Ui_CalcWindow
        from preset_management import view_presets
        global password
        password = self.pwd_input
        try:
            if check_password(password):
                con = ms.connect(host = "localhost", user = "root", passwd = password)
                global cur
                cur = con.cursor()
            cur.execute('use alphacalc')
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_CalcWindow()
            self.ui.variable = password
            self.ui.setupUi(self.window)
            begin(password)
            begin_eval(password)
            new_temp(password)
            cur.execute('select * from memory')
            data=cur.fetchall()
            if any(data):
                for x in data:
                        row_count=self.ui.Mem_Display.rowCount()
                        self.ui.Mem_Display.setRowCount(row_count+1)
                        self.ui.Mem_Display.setItem(row_count,0,QtWidgets.QTableWidgetItem(str(x[0])))
                        self.ui.Mem_Display.setItem(row_count,1,QtWidgets.QTableWidgetItem(str(x[1])))
                        self.ui.Mem_Display.setItem(row_count,2,QtWidgets.QTableWidgetItem(x[2]))
                        self.ui.Mem_Display.setItem(row_count,3,QtWidgets.QTableWidgetItem(str(x[3])))
            presets=view_presets(password)
            for y in presets:
                row_count=self.ui.Display.rowCount()
                self.ui.Display.setRowCount(row_count+1)
                self.ui.Display.setItem(row_count,0,QtWidgets.QTableWidgetItem(y[0]))
                self.ui.Display.setItem(row_count,1,QtWidgets.QTableWidgetItem(y[1]))
                self.ui.Display.setItem(row_count,2,QtWidgets.QTableWidgetItem(y[2]))
                self.ui.Display.setItem(row_count,3,QtWidgets.QTableWidgetItem(y[3]))
            self.window.show()
            LoginWindow.hide()
        except Exception:
            self.hide.setHidden(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())
