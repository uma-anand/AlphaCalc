from PyQt5.QtWidgets import QMainWindow , QApplication , QLabel , QTabWidget , QTableWidget , QPushButton , QLineEdit , QPlainTextEdit , QWidget , QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import mysql.connector as ms 
from datetime import date,datetime
from expression_evaluation import *
from start_up import relative_to_bg
from preset_management import add_preset , delete_preset , search

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator,self).__init__()
        uic.loadUi('calculator.ui',self) 

        self.Tabs = self.findChild(QTabWidget,'Tabs')
        self.variable = ''

        # Tab 1
        self.tab_1 = self.findChild(QWidget,'tab_1')
        self.View_Presets = self.findChild(QLabel,'View_Presets')
        self.View_Presets.setPixmap(QPixmap(str(relative_to_bg("View Presets.jpg"))))
        self.Display = self.findChild(QTableWidget,'Display')
        self.Display.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n""font: 75 12pt \"Courier New\";\n")
        self.Display.setColumnCount(4)
        self.Display.verticalHeader().setVisible(False)
        self.Display.setHorizontalHeaderLabels(['Type','Translation','Operation Part 1','Operation Part 2'])
        self.Display.setColumnWidth(0,100)
        self.Display.setColumnWidth(1,130)
        self.Display.setColumnWidth(2,210)
        self.Display.setColumnWidth(3,210)

        # Tab 2
        self.tab_2 = self.findChild(QWidget,'tab_2')
        self.Edit_Presets = self.findChild(QLabel,'Edit_Presets')
        self.Edit_Presets.setPixmap(QPixmap(str(relative_to_bg("Edit Presets.jpg"))))
        self.Input_1 = self.findChild(QLineEdit,'Input_1')
        self.Input_2 = self.findChild(QLineEdit,'Input_2')
        self.Input_3 = self.findChild(QLineEdit,'Input_3')
        self.Input_4 = self.findChild(QLineEdit,'Input_4')
        self.Input_5 = self.findChild(QLineEdit,'Input_5')
        self.Input_6 = self.findChild(QLineEdit,'Input_6')
        self.Erase_But = self.findChild(QPushButton,'Erase_But')
        self.Erase_But.clicked.connect(self.clear)
        self.Add_But = self.findChild(QPushButton,'Add_But')
        self.Add_But.clicked.connect(self.add)
        self.Del_But_2 = self.findChild(QPushButton,'Del_But_2')
        self.Del_But_2.clicked.connect(self.remove)

        # Tab 3
        self.tab_3 = self.findChild(QWidget,'tab_3')
        self.Search = self.findChild(QLabel,'Search')
        self.Search.setPixmap(QPixmap(str(relative_to_bg("Search.jpg"))))
        self.Keyword = self.findChild(QLineEdit,'Keyword')
        self.Result = self.findChild(QTableWidget,'Result')
        self.Result.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n""font: 75 12pt \"Courier New\";\n")
        self.Result.setColumnCount(4)
        self.Result.verticalHeader().setVisible(False)
        self.Result.setHorizontalHeaderLabels(['Type','Translation','Operation Part 1','Operation Part 2'])
        self.Result.setColumnWidth(0,100)
        self.Result.setColumnWidth(1,130)
        self.Result.setColumnWidth(2,210)
        self.Result.setColumnWidth(3,210)
        self.Search_But = self.findChild(QPushButton,'Search_But')
        self.Search_But.clicked.connect(self.result)

        # Tab 4
        self.tab_4 = self.findChild(QWidget,'tab_4')
        self.Calculator = self.findChild(QLabel,'Calculator')
        self.Calculator.setPixmap(QPixmap(str(relative_to_bg("Calculator.jpg"))))
        self.Answer = self.findChild(QLabel,'Answer')
        self.Expression = self.findChild(QPlainTextEdit,'Expression')
        self.Message = self.findChild(QLabel,'Message')
        self.Eval_But = self.findChild(QPushButton,'Eval_But')
        self.Eval_But.clicked.connect(self.calculate)
        self.Clear_But = self.findChild(QPushButton,'Clear_But')
        self.Clear_But.clicked.connect(self.clear)
        self.Speak_But = self.findChild(QPushButton,'Speak_But')
        self.Speak_But.clicked.connect(self.audio_input)

        # Tab 5
        self.tab_5 = self.findChild(QWidget,'tab_5')
        self.Memory = self.findChild(QLabel,'Memory')
        self.Memory.setPixmap(QPixmap(str(relative_to_bg("Memory.jpg"))))
        self.Mem_Display = self.findChild(QTableWidget,'Mem_Display')
        self.Mem_Display.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n""font: 75 12pt \"Courier New\";\n")
        self.Mem_Display.setColumnCount(4)
        self.Mem_Display.verticalHeader().setVisible(False)
        self.Mem_Display.setHorizontalHeaderLabels(['Date','Time','Expression','Answer'])
        self.Mem_Display.setColumnWidth(0,110)
        self.Mem_Display.setColumnWidth(1,100)
        self.Mem_Display.setColumnWidth(2,274)
        self.Mem_Display.setColumnWidth(3,75)
        self.Del_But = self.findChild(QPushButton,'Del_But')
        self.Del_But.clicked.connect(self.delete)

        self.show()


    def clear(self):
            self.Expression.clear()
            self.Answer.setText("")
            self.Message.setText("")
            self.Input_1.setText("")
            self.Input_2.setText("")
            self.Input_3.setText("")
            self.Input_4.setText("")
            self.Input_5.setText("")
            self.Input_6.setText("")

    def calculate(self):
            n=self.Expression.toPlainText()
            ans=str(evaluation(n))
            if self.Expression.toPlainText() != '':
                self.Answer.setText(str(ans))
            d=str(date.today())
            t=str(datetime.now().strftime("%H:%M:%S"))
            data=(d,t,n,ans)
            db = ms.connect(host = "localhost", user = "root", passwd = self.variable)
            cur = db.cursor()
            cur.execute('use alphacalc')
            query='insert into Memory values(%s,%s,%s,%s)'
            cur.execute(query,data)
            db.commit()
            row_count=self.Mem_Display.rowCount()
            self.Mem_Display.setRowCount(row_count+1)
            self.Mem_Display.setItem(row_count,0,QTableWidgetItem(d))
            self.Mem_Display.setItem(row_count,1,QTableWidgetItem(t))
            self.Mem_Display.setItem(row_count,2,QTableWidgetItem(n))
            self.Mem_Display.setItem(row_count,3,QTableWidgetItem(ans))
            return ans

    def delete(self):
            db = ms.connect(host = "localhost", user = "root", passwd = self.variable)
            cur = db.cursor()
            cur.execute('use alphacalc')
            cur.execute('delete from memory')
            db.commit()
            self.Mem_Display.setRowCount(0)

    def audio_input(self):
            from speech_recognition import Recognizer,Microphone
            rec=Recognizer()
            mic=Microphone()
            with mic as audio_file:
                rec.adjust_for_ambient_noise(audio_file,duration=5)
                self.Message.setText('Start Speaking')
                audio=rec.listen(audio_file)
                try:
                        speech=rec.recognize_google(audio)
                        result=self.calculate(speech)
                        self.audio_output(result)
                except Exception:
                       self.Message.setText('Try Again')

    def audio_output(self,text):
            from os import remove
            from gtts import gTTS
            from playsound import playsound
            output=gTTS(text=text,lang='en',slow=False)
            output.save('answer.mp3')
            playsound('answer.mp3') 
            remove('answer.mp3')         
                  
    def add(self):
            add_preset(self.Input_1.text(),self.Input_3.text(),self.Input_4.text(),self.Input_2.text(), self.variable)
            row_count=self.Display.rowCount()
            self.Display.setRowCount(row_count+1)
            self.Display.setItem(row_count,0,QTableWidgetItem(self.Input_1.text()))
            self.Display.setItem(row_count,1,QTableWidgetItem(self.Input_2.text()))
            self.Display.setItem(row_count,2,QTableWidgetItem(self.Input_3.text()))
            self.Display.setItem(row_count,3,QTableWidgetItem(self.Input_4.text()))
            
    def remove(self):
            delete_preset(self.Input_5.text(),self.Input_6.text(), self.variable)
            row_no=(self.Display.findItems(self.Input_5.text(),Qt.MatchFlag.MatchExactly))[0].row()
            self.Display.removeRow(row_no)

    def result(self):
            kw = self.Keyword.text()
            result = search(kw,self.variable) 
            self.Result.setRowCount(0)
            for x in result:
                row_count=self.Result.rowCount()
                self.Result.setRowCount(row_count+1)
                self.Result.setItem(row_count,0,QTableWidgetItem(x[0]))
                self.Result.setItem(row_count,1,QTableWidgetItem(x[1]))
                self.Result.setItem(row_count,2,QTableWidgetItem(x[2]))
                self.Result.setItem(row_count,3,QTableWidgetItem(x[3]))
               

CalcApp = QApplication(sys.argv)
CalcWindow = Calculator()
