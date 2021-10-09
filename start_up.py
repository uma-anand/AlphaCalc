import mysql.connector as ms
import sys

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
        sys.exit()

def exists(database):
    cur.execute("show databases")
    data = cur.fetchall()
    for x in data:
        if database in x:
            return True
    return False

def use_presets():
    if not exists("presets"):
        cur.execute("create database presets")
        cur.execute("use presets")
    else:
        cur.execute("drop database presets")
        use_presets()

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


