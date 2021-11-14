
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import mysql.connector as ms 
from datetime import date,datetime


def relative_to_bg(path: str) -> Path:
        return BG_PATH / Path(path)
OUTPUT_PATH = Path(__file__).parent
BG_PATH = OUTPUT_PATH / Path("./backgrounds")

class Ui_CalcWindow(object):

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

    def calculate(self,n):
            from expression_evaluation import evaluation
            ans=evaluation(n)
            if self.Expression.toPlainText() != '':
                self.Answer.setText(str(ans))
            d=str(date.today())
            t=str(datetime.now().strftime("%H:%M:%S"))
            data=(d,t,n,ans)
            password = input('Enter password:')
            db = ms.connect(host = "localhost", user = "root", passwd = password)
            cur = db.cursor()
            cur.execute('use alphacalc')
            query='insert into Memory values(%s,%s,%s,%s)'
            cur.execute(query,data)
            db.commit()
            row_count=self.Mem_Display.rowCount()
            self.Mem_Display.setRowCount(row_count+1)
            self.Mem_Display.setItem(row_count,0,QtWidgets.QTableWidgetItem(d))
            self.Mem_Display.setItem(row_count,1,QtWidgets.QTableWidgetItem(t))
            self.Mem_Display.setItem(row_count,2,QtWidgets.QTableWidgetItem(n))
            self.Mem_Display.setItem(row_count,3,QtWidgets.QTableWidgetItem(ans))
            return ans

    def delete(self):
            password = input('Enter password:')
            db = ms.connect(host = "localhost", user = "root", passwd = password)
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
            from preset_management import add_preset
            add_preset(self.Input_1.text(),self.Input_3.text(),self.Input_4.text(),self.Input_2.text())
            row_count=self.Display.rowCount()
            self.Display.setRowCount(row_count+1)
            self.Display.setItem(row_count,0,QtWidgets.QTableWidgetItem(self.Input_1.text()))
            self.Display.setItem(row_count,1,QtWidgets.QTableWidgetItem(self.Input_3.text()))
            self.Display.setItem(row_count,2,QtWidgets.QTableWidgetItem(self.Input_4.text()))
            self.Display.setItem(row_count,3,QtWidgets.QTableWidgetItem(self.Input_2.text()))
            
    def remove(self):
            from preset_management import delete_preset
            delete_preset(self.Input_5.text(),self.Input_6.text())
            row_no=(self.Display.findItems(self.Input_5.text(),QtCore.Qt.MatchFlag.MatchExactly))[0].row()
            self.Display.removeRow(row_no)    

    def setupUi(self, CalcWindow):
        CalcWindow.setObjectName("CalcWindow")
        CalcWindow.resize(500, 529)
        self.centralwidget = QtWidgets.QWidget(CalcWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.Tabs.setGeometry(QtCore.QRect(0, 0, 500, 511))
        self.Tabs.setObjectName("Tabs")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.About = QtWidgets.QLabel(self.tab_1)
        self.About.setGeometry(QtCore.QRect(0, 0, 500, 489))
        self.About.setText("")
        self.About.setPixmap(QtGui.QPixmap(str(relative_to_bg("About.jpg"))))
        self.About.setObjectName("About")
        self.Tabs.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.Instructions = QtWidgets.QLabel(self.tab_2)
        self.Instructions.setGeometry(QtCore.QRect(0, 0, 500, 489))
        self.Instructions.setText("")
        self.Instructions.setPixmap(QtGui.QPixmap(str(relative_to_bg("Instructions.jpg"))))
        self.Instructions.setObjectName("Instructions")
        self.Tabs.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.View_Presets = QtWidgets.QLabel(self.tab_3)
        self.View_Presets.setGeometry(QtCore.QRect(0, 0, 500, 487))
        self.View_Presets.setText("")
        self.View_Presets.setPixmap(QtGui.QPixmap(str(relative_to_bg("View Presets.jpg"))))
        self.View_Presets.setObjectName("View_Presets")
        self.Display = QtWidgets.QLabel(self.tab_3)
        self.Display.setGeometry(QtCore.QRect(35, 130, 430, 315))
        self.Display.setStyleSheet("background-color: (212, 252, 255, 1);\n"
"font: italic 16pt \"Courier New\";")
        self.Display.setText("")
        self.Display.setObjectName("Display")
        self.Tabs.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.Edit_Presets = QtWidgets.QLabel(self.tab_4)
        self.Edit_Presets.setGeometry(QtCore.QRect(0, 0, 500, 489))
        self.Edit_Presets.setText("")
        self.Edit_Presets.setPixmap(QtGui.QPixmap(str(relative_to_bg("Edit Presets.jpg"))))
        self.Edit_Presets.setObjectName("Edit_Presets")
        self.Input_1 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_1.setGeometry(QtCore.QRect(36, 189, 191, 31))
        self.Input_1.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_1.setFrame(False)
        self.Input_1.setObjectName("Input_1")
        self.Input_2 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_2.setGeometry(QtCore.QRect(250, 189, 221, 31))
        self.Input_2.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_2.setFrame(False)
        self.Input_2.setObjectName("Input_2")
        self.Input_3 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_3.setGeometry(QtCore.QRect(36, 255, 191, 31))
        self.Input_3.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_3.setFrame(False)
        self.Input_3.setObjectName("Input_3")
        self.Input_4 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_4.setGeometry(QtCore.QRect(250, 255, 221, 31))
        self.Input_4.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_4.setFrame(False)
        self.Input_4.setObjectName("Input_4")
        self.Input_5 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_5.setGeometry(QtCore.QRect(36, 374, 191, 31))
        self.Input_5.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_5.setFrame(False)
        self.Input_5.setObjectName("Input_5")
        self.Input_6 = QtWidgets.QLineEdit(self.tab_4)
        self.Input_6.setGeometry(QtCore.QRect(250, 374, 221, 31))
        self.Input_6.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 11pt \"Courier New\";\n"
"")
        self.Input_6.setFrame(False)
        self.Input_6.setObjectName("Input_6")
        self.Add_But = QtWidgets.QPushButton(self.tab_4,clicked=lambda:self.add())
        self.Add_But.setGeometry(QtCore.QRect(193, 426, 111, 31))
        self.Add_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Add_But.setObjectName("Add_But")
        self.Erase_But = QtWidgets.QPushButton(self.tab_4,clicked=lambda:self.clear())
        self.Erase_But.setGeometry(QtCore.QRect(40, 426, 111, 31))
        self.Erase_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Erase_But.setObjectName("Erase_But")
        self.Remove_But = QtWidgets.QPushButton(self.tab_4,clicked=lambda:self.remove())
        self.Remove_But.setGeometry(QtCore.QRect(350, 426, 111, 31))
        self.Remove_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Remove_But.setObjectName("Remove_But")
        self.Tabs.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.Calculator = QtWidgets.QLabel(self.tab_5)
        self.Calculator.setGeometry(QtCore.QRect(0, 0, 500, 489))
        self.Calculator.setText("")
        self.Calculator.setPixmap(QtGui.QPixmap(str(relative_to_bg("Calculator.jpg"))))
        self.Calculator.setObjectName("Calculator")
        self.Expression = QtWidgets.QPlainTextEdit(self.tab_5)
        self.Expression.setGeometry(QtCore.QRect(35, 170, 431, 71))
        self.Expression.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 12pt \"Courier New\";\n"
"")
        self.Expression.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Expression.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Expression.setLineWidth(7)
        self.Expression.setObjectName("Expression")
        self.Answer = QtWidgets.QLabel(self.tab_5)
        self.Answer.setGeometry(QtCore.QRect(40, 310, 421, 31))
        self.Answer.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 12pt \"Courier New\";\n"
"")
        self.Answer.setText("")
        self.Answer.setObjectName("Answer")
        self.Clear_But = QtWidgets.QPushButton(self.tab_5, clicked=lambda:self.clear())
        self.Clear_But.setGeometry(QtCore.QRect(197, 393, 111, 31))
        self.Clear_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Clear_But.setObjectName("Clear_But")
        self.Eval_But = QtWidgets.QPushButton(self.tab_5,clicked=lambda:self.calculate(self.Expression.toPlainText()))
        self.Eval_But.setGeometry(QtCore.QRect(44, 393, 111, 31))
        self.Eval_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Eval_But.setObjectName("Eval_But")
        self.Speak_But = QtWidgets.QPushButton(self.tab_5,clicked=lambda:self.audio_input())
        self.Speak_But.setGeometry(QtCore.QRect(348, 393, 111, 31))
        self.Speak_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Speak_But.setObjectName("Speak_But")
        self.Message = QtWidgets.QLabel(self.tab_5)
        self.Message.setGeometry(QtCore.QRect(140, 439, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Message.setFont(font)
        self.Message.setStyleSheet("background-color: rgba(135, 254, 225, 1);\n"
"")
        self.Message.setAlignment(QtCore.Qt.AlignCenter)
        self.Message.setObjectName("Message")
        self.Tabs.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.Memory = QtWidgets.QLabel(self.tab_6)
        self.Memory.setGeometry(QtCore.QRect(0, 0, 500, 489))
        self.Memory.setText("")
        self.Memory.setPixmap(QtGui.QPixmap(str(relative_to_bg("Memory.jpg"))))
        self.Memory.setObjectName("Memory")
        self.Mem_Display = QtWidgets.QTableWidget(self.tab_6)
        self.Mem_Display.setGeometry(QtCore.QRect(40, 130, 421, 251))
        self.Mem_Display.setStyleSheet("background-color: rgba(212, 252, 255, 1);\n"
"font: 75 12pt \"Courier New\";\n"
"")
        self.Mem_Display.setObjectName("Mem_Display")
        self.Mem_Display.setColumnCount(4)
        self.Mem_Display.verticalHeader().setVisible(False)
        self.Mem_Display.setHorizontalHeaderLabels(['Date','Time','Expression','Answer'])
        self.Mem_Display.setColumnWidth(0,75)
        self.Mem_Display.setColumnWidth(1,75)
        self.Mem_Display.setColumnWidth(2,194)
        self.Mem_Display.setColumnWidth(3,75)
        self.Del_But = QtWidgets.QPushButton(self.tab_6,clicked=lambda:self.delete())
        self.Del_But.setGeometry(QtCore.QRect(173, 405, 171, 31))
        self.Del_But.setStyleSheet("font: 87 15pt \"Arial Black\";\n"
"background-color: rgba(170, 163, 255, 1);\n"
"")
        self.Del_But.setObjectName("Del_But")
        self.Tabs.addTab(self.tab_6, "")
        CalcWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CalcWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        CalcWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CalcWindow)
        self.statusbar.setObjectName("statusbar")
        CalcWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CalcWindow)
        self.Tabs.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(CalcWindow)

    def retranslateUi(self, CalcWindow):
        _translate = QtCore.QCoreApplication.translate
        CalcWindow.setWindowTitle(_translate("CalcWindow", "AlphaCalc"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_1), _translate("CalcWindow", "About"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_2), _translate("CalcWindow", "Instructions"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_3), _translate("CalcWindow", "View Presets"))
        self.Add_But.setText(_translate("CalcWindow", "Add"))
        self.Erase_But.setText(_translate("CalcWindow", "Clear"))
        self.Remove_But.setText(_translate("CalcWindow", "Delete"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_4), _translate("CalcWindow", "Edit Presets"))
        self.Clear_But.setText(_translate("CalcWindow", "Clear"))
        self.Eval_But.setText(_translate("CalcWindow", "Evaluate"))
        self.Speak_But.setText(_translate("CalcWindow", "Speak"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_5), _translate("CalcWindow", "Calculator"))
        self.Del_But.setText(_translate("CalcWindow", "Clear Memory"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.tab_6), _translate("CalcWindow", "Memory"))
        QtCore.pyqtRemoveInputHook()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CalcWindow = QtWidgets.QMainWindow()
    ui = Ui_CalcWindow()
    ui.setupUi(CalcWindow)
    CalcWindow.show()
    sys.exit(app.exec_())
