from tkinter import *
from tkinter import ttk
import mysql.connector as ms

two_part_operations = {"type":"two_part_operations", "divide":"by", "multiply":"with", "add":"with", "subtract":"from"}
operations_translations = {"type":"operations_translations","divide":"/", "multiply":"*", "add":"+", "subtract":"-"}
like_add = {"type":"like_add","divide":"/", "multiply":"*", "add":"+"}
like_subtract = {"type":"like_subtract","subtract":"-"}
like_exp = {"type":"like_exp","to the power of":"**", "^":"**", "multiplied by": "*", "divided by": "/", "multiplied with": "*", 
            "added with": "+", "subtracted by":"-", "greater than or equal to": ">=", "is greater than":">","greater than":">", 
            "lesser than or equal to": "<=", "is lesser than":"<", "lesser than":"<", "is equal to":"==", "equal to":"=="}
operations_overall =  {"type":"operations_overall", "multiplied by": "*", "divided by": "/", "multiplied with": "*", "added with": "+", 
                "subtracted by":"-", "divide":"by", "multiply":"with", "add":"with", "subtract":"from", "to the power of":"**",
                "^":"**",  "greater than or equal to": ">=", "is greater than":">","greater than":">", "lesser than or equal to": "<=",
                "is lesser than":"<", "lesser than":"<", "is equal to":"==", "equal to":"==" }
overall = [two_part_operations, operations_translations, like_add, like_subtract, like_exp, operations_overall]
overall_names = ["two_part_operations", "operations_translations", "like_add", "like_subtract", "like_exp", "operations_overall"]
 
def check_password(password):
    try:
        global con, cur
        con = ms.connect(host = "localhost", user = "root", passwd = password)
        cur = con.cursor()
    except Exception:
        print('Invalid Password')

def delete_temp():
    for x in overall_names:
        a = "drop table temp_"+x
        cur.execute(a)
        con.commit()

def exists(database):
    cur.execute("show databases")
    data = cur.fetchall()
    for x in data:
        if database in x:
            return True
    return False

def create_table(tablename):
    b = "create table "+ tablename+" (operation_name varchar(50), operation varchar(50))"
    cur.execute(b)
    ind = overall_names.index(tablename)
    corr_dict = overall[ind]
    for x in corr_dict:
        a = "insert into "+tablename+ " values ( '"+ x+"', '"+ corr_dict[x]+"')"
        cur.execute(a)
        con.commit()

def create_presets():
    for y in overall_names:
        create_table(y)

def temp_exists():
    cur.execute("show tables")
    data = cur.fetchall()
    if "temp_like_exp" in data:
        return True
    return False

def create_temp():
    for tablename in overall_names:
        c = "create table temp_"+tablename+ " (operation_name varchar(50), operation varchar(50))"
        cur.execute(c)
        a = "insert into temp_"+tablename+ " select * from "+tablename
        cur.execute(a)
        con.commit()

def add_preset(types, operation_name, operation):
    for x in types:
        a = 'insert into '+x+' values ("'+operation_name+'", "'+operation+'")'
        cur.execute(a)
        a = 'insert into temp_'+x+' values ("'+operation_name+'", "'+operation+'")'
        cur.execute(a)

def create_all():
    if not exists("presets"):
        cur.execute("create database presets")
        cur.execute("use presets")
        create_presets()
    else:
        cur.execute("use presets")
    if temp_exists:
        delete_temp()
    create_temp()

check_password("awesomeisuma123")
create_all()

'''
data will be of form
[('type', 'like_add'), ('divide', '/'), ('multiply', '*'), ('add', '+')]
'''

def update_dicts():
    for x in overall_names:
        a = "select * from "+x
        ind = overall_names.index(x)
        corr_dict = overall[ind]
        cur.execute(a)
        data = cur.fetchall()
        corr_dict = {}
        for tup in data:
            corr_dict[tup[0]] = tup[1]
        if x == "two_part_operations":
            two_part_operations.clear()
            two_part_operations.update(corr_dict)
        elif x == "operations_translations":
            operations_translations.clear()
            operations_translations.update(corr_dict)
        elif x == "like_add":
            like_add.clear()
            like_add.update(corr_dict)
        elif x == "like_subtract":
            like_subtract.clear()
            like_subtract.update(corr_dict)
        elif x == "like_exp":
            like_exp.clear()
            like_exp.update(corr_dict)
        elif x == "operations_overall":
            operations_overall.clear()
            operations_overall.update(corr_dict)

update_dicts()

#calculates expression given the input multiply 3 by 4 or 
 
def translate_operations(phrase):
    for a in operations_overall:
        if a in phrase:
            operation = a
            break
    else:
        return phrase
    if operation not in like_exp:
        sub_ind = phrase.index(two_part_operations[a])
    operation_ind = phrase.index(a)
    if operation in like_add:
        to_eval = phrase[operation_ind+len(operation):sub_ind:]+operations_translations[operation]+phrase[sub_ind+len(two_part_operations[operation])::]
    elif operation in like_subtract:
        to_eval = phrase[sub_ind+len(two_part_operations[operation])::]+operations_translations[operation]+phrase[operation_ind+len(operation):sub_ind:]
    elif operation in like_exp:
        to_eval = phrase[:operation_ind:]+like_exp[operation]+phrase[operation_ind+len(operation)::]
    return to_eval
 
 # split the expression into smaller fragments

def split_expression(expression):
    from re import split
    fragments=list(filter(None,split(r'[()]',expression)))
    translated=[]
    for x in fragments:
        translated+=[translate_operations(x)]
    ans=''
    for x,y in zip(fragments,translated):
        ans=expression.replace(x,y)
        expression=ans
    return eval(str(ans))

def addbrackets(express):
    expression = express
    a = expression.find(")")
    if a!=-1:
        expression = expression[a+1::]
    for a in expression:
        if a.isdigit():
            first_num = expression.index(a)
            break
    temp = expression[first_num::]
    for a in temp:
        if not a.isdigit():
            first_char = temp.index(a)
            break
    temp = temp[first_char::]
    first_char+=first_num
    for a in temp:
        if a.isdigit():
            second_num = temp.index(a)
            break
    temp = temp[second_num::]
    second_num+=first_char
    for a in temp:
        if not a.isdigit():
            second_char = temp.index(a)
            break
    else:
        second_char = len(temp)
    second_char+=second_num
    new_expression = str(eval(translate_operations(expression[:second_char:])))+expression[second_char::]
    try:
        return split_expression(new_expression)
    except SyntaxError:
        return addbrackets(new_expression)

def evaluation(expression):
    try:
        return split_expression(expression)
    except SyntaxError:
        return addbrackets(expression)


 
def audio():
    # To Convert Speech to Text
    from speech_recognition import Recognizer,Microphone
    rec=Recognizer()
    mic=Microphone()
    txt=''
    with mic as audio_file:
        rec.adjust_for_ambient_noise(audio_file)
        audio=rec.listen(audio_file)
        try:
            speech=rec.recognize_google(audio)
            try:
                txt=evaluation(speech)
            except Exception:
                txt=str(eval(speech))
            # To Convert Text to Speech
            from os import remove
            from gtts import gTTS
            from playsound import playsound
            output=gTTS(text=txt,lang='en',slow=False)
            output.save('answer.mp3')
            playsound('answer.mp3') 
            remove('answer.mp3')
        except Exception:
          answer.set('Try Again')
 
 
def home():
    # GUI
    
    main=Tk()
    main.title('AlphaCalc')
    main.geometry('500x500')
    tabs=ttk.Notebook(main)
    global answer
    answer=StringVar()
    
    # Clear the Text and Label Widgets
    def clear():
        exp.delete(1.0,END)
        answer.set('')
    
    # Display the answer
    def evaluate():
        ex=exp.get('1.0','end-1c')
        answer.set(evaluation(ex))
    
    # Homepage
    home=Frame(tabs,bg='light pink')
    tabs.add(home,text='Home')
    Label(home,text='AlphaCalc',bg='light pink',font=('Times New Roman',50,'bold')).place(x=80,y=100)
    
    # Intructions
    inst=Frame(tabs,bg='light blue')
    tabs.add(inst,text='Instructions')
    Label(inst,text='Instructions',bg='light blue',font=('Times New Roman',30,'bold'),anchor=CENTER).pack()
    
    # Settings
    sett=Frame(tabs,bg='light green')
    tabs.add(sett,text='Settings')
    Label(sett,text='Settings',bg='light green',font=('Times New Roman',30,'bold'),anchor=CENTER).pack()
    
    # Calculator
    calc=Frame(tabs,bg='light yellow')
    tabs.add(calc,text='Calculator')
    Label(calc,text='Calculator',bg='light yellow',font=('Times New Roman',30,'bold'),anchor=CENTER).pack()
    Label(calc,text='Expression :',bg='light yellow',font=('Times New Roman',15,'bold')).place(x=20,y=50)
    exp=Text(calc,font=('Times New Roman',15),height=5,width=25)
    exp.place(x=150,y=50)
    Label(calc,text='Answer :',bg='light yellow',font=('Times New Roman',15,'bold')).place(x=20,y=200)
    Label(calc,textvariable=answer,font=('Times New Roman',15,'normal'),bg='light yellow',bd=0).place(x=150,y=200)
    Button(calc,text='Evaluate',bg='light blue',font=('Times New Roman',15,'normal'),command=lambda:evaluate()).place(x=60,y=300)
    Button(calc,text='Clear',bg='light blue',font=('Times New Roman',15,'normal'),command=lambda:clear()).place(x=200,y=300)
    Button(calc,text='Speak',bg='light blue',font=('Times New Roman',15,'normal'),command=lambda:audio()).place(x=300,y=300)
    
    tabs.pack(expand=1,fill='both')
    main.mainloop()

def incorrect_password():
    # Figma
    # This file was generated by the Tkinter Designer by Parth Jadhav
    # https://github.com/ParthJadhav/Tkinter-Designer
    
    
    from pathlib import Path
    
    # from tkinter import *
    # Explicit imports to satisfy Flake8
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
    
    
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    
    
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    
    window = Tk()
    
    window.geometry("342x447")
    window.configure(bg = "#FFFFFF")
    
    
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 447,
        width = 342,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        342.0,
        447.0,
        fill="#FFFFFF",
        outline="")
    
    canvas.create_rectangle(
        0.0,
        303.0,
        342.0,
        447.0,
        fill="#000000",
        outline="")
    
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        171.0,
        151.0,
        image=image_image_1
    )
    
    canvas.create_text(
        8.000000000000028,
        322.0,
        anchor="nw",
        text="Enter your password:",
        fill="#FFF3F3",
        font=("RoundedMplus1c Bold", 14 * -1)
    )
    
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        247.00000000000003,
        332.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FF7C7C",
        highlightthickness=0
    )
    entry_1.place(
        x=165.00000000000003,
        y=322.0,
        width=164.0,
        height=19.0
    )
    
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=113.00000000000003,
        y=363.0,
        width=116.0,
        height=35.0
    )
    
    canvas.create_text(
        18.00000000000003,
        412.0,
        anchor="nw",
        text="Incorrect mySQL password. Please try again.",
        fill="#FFFFFF",
        font=("RoundedMplus1c Bold", 14 * -1)
    )
    window.resizable(False, False)
    window.mainloop() 

def password(): 
    # This file was generated by the Tkinter Designer by Parth Jadhav
    # https://github.com/ParthJadhav/Tkinter-Designer
    
    
    from pathlib import Path
    
    # from tkinter import *
    # Explicit imports to satisfy Flake8
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
    
    
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    
    
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    
    window = Tk()
    
    window.geometry("342x412")
    window.configure(bg = "#FFFFFF")
    
    
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 412,
        width = 342,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        342.0,
        412.0,
        fill="#FFFFFF",
        outline="")
    
    canvas.create_rectangle(
        0.0,
        303.0,
        342.0,
        412.0,
        fill="#000000",
        outline="")
    
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        171.0,
        151.0,
        image=image_image_1
    )
    
    canvas.create_text(
        8.0,
        322.0,
        anchor="nw",
        text="Enter your password:",
        fill="#FFF3F3",
        font=("RoundedMplus1c Bold", 14 * -1)
    )
    
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        247.0,
        332.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFD2D2",
        highlightthickness=0
    )
    entry_1.place(
        x=165.0,
        y=322.0,
        width=164.0,
        height=19.0
    )
    
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=113.0,
        y=363.0,
        width=116.0,
        height=35.0
    )
    window.resizable(False, False)
    window.mainloop()

password()
incorrect_password()
home() 

 

