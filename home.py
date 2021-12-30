from PyQt5.QtWidgets import QMainWindow , QApplication , QLabel , QLineEdit , QPushButton , QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys 
import mysql.connector as ms
from expression_evaluation import begin_eval
from preset_management import begin, new_temp, view_presets
from start_up import check_password, relative_to_bg, use_presets

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__() 
        uic.loadUi('home.ui',self)

        self.bg = self.findChild(QLabel,'bg')
        self.msg = self.findChild(QLabel,'hide')
        self.pwd_input = self.findChild(QLineEdit,'pwd_input')
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.submit = self.findChild(QPushButton,'submit')

        self.bg.setPixmap(QPixmap(str(relative_to_bg("bg.jpg"))))
        self.submit.clicked.connect(self.login)

        self.show()

    def login(self):
        from calculator import CalcWindow
        global password
        password = self.pwd_input.text()
        try:
                if check_password(password):
                        con = ms.connect(host = "localhost", user = "root", passwd = password)
                        global cur
                        cur = con.cursor()
                self.window = CalcWindow
                self.window.variable = password
                begin(password)
                new_temp(password)
                begin_eval(password)
                cur.execute('use alphacalc')
                cur.execute('select * from memory')
                data=cur.fetchall()
                if any(data):
                        for x in data:
                                row_count=self.window.Mem_Display.rowCount()
                                self.window.Mem_Display.setRowCount(row_count+1)
                                self.window.Mem_Display.setItem(row_count,0,QTableWidgetItem(str(x[0])))
                                self.window.Mem_Display.setItem(row_count,1,QTableWidgetItem(str(x[1])))
                                self.window.Mem_Display.setItem(row_count,2,QTableWidgetItem(x[2]))
                                self.window.Mem_Display.setItem(row_count,3,QTableWidgetItem(str(x[3])))
                presets=view_presets(password)
                for y in presets:
                        row_count=self.window.Display.rowCount()
                        self.window.Display.setRowCount(row_count+1)
                        self.window.Display.setItem(row_count,0,QTableWidgetItem(y[0]))
                        self.window.Display.setItem(row_count,1,QTableWidgetItem(y[1]))
                        self.window.Display.setItem(row_count,2,QTableWidgetItem(y[2]))
                        self.window.Display.setItem(row_count,3,QTableWidgetItem(y[3]))
                self.window.show()
                LoginWindow.setHidden(True)
        except Exception:
            self.msg.setHidden(True)

LoginApp = QApplication(sys.argv)
LoginWindow = HomePage()
LoginApp.exec_()
