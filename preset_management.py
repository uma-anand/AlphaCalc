from start_up import *

password = input("Enter password: ")
check_password(password)
use_presets()
create_presets()

con = ms.connect(host = "localhost", user = "root", passwd = password)
cur = con.cursor()
cur.execute("use presets")

def delete_temp():
    for x in overall_names:
        a = "drop table temp_"+x
        cur.execute(a)
        con.commit()

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

'''
data will be of form
[('type', 'like_add'), ('divide', '/'), ('multiply', '*'), ('add', '+')]
'''

def update_dicts():
    for x in overall_names:
        a = "select * from temp_"+x
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

