from start_up import *

password = input("Enter password: ")
check_password(password)
use_presets()
create_presets()

con = ms.connect(host = "localhost", user = "root", passwd = password)
cur = con.cursor()
cur.execute("use presets")

def delete_temp():
    a = "drop table temp_operations"
    cur.execute(a)
    con.commit()

def temp_exists():
    cur.execute("show tables")
    data = cur.fetchall()
    if "temp_operations" in data:
        return True
    return False

def create_temp():
    c = "create table temp_operations (type varchar(1), translation varchar (10), operation_part_1 varchar(50), operation_part_2 varchar(50))"
    cur.execute(c)
    a = "insert into temp_operations select * from operations"
    cur.execute(a)
    con.commit()

def add_preset(type, part_1, part_2, translation):
        a = "insert into temp_operations values ( '%s', '%s', '%s', '%s' )" %(type, part_1, part_2, translation)
        cur.execute(a)
        con.commit()

def delete_preset(part_1,part_2):
    a = "delete from temp_operations where operation_part_1 = '%s' and operation_part_2 = '%s'" %(part_1, part_2)
    cur.execute(a)
    con.commit()

'''
data will be of form
The columns will be Type, Translation, Operation Part 1, Operation Part 2
[("2", "/", "divide","by"), ("2", "*", "multiply","with"), ("2", "*", "multiply","by")...]
'''

def update_dicts():
    a = "select * from temp_operations"
    cur.execute(a)
    global operations
    operations = cur.fetchall()
        
def view_presets():
    a = "select * from temp_operations"
    cur.execute(a)
    return cur.fetchall()


