from start_up import *

def begin(password):
    check_password(password)
    use_presets()
    create_presets()

def delete_temp(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    a = "drop table temp_operations"
    cur.execute(a)
    con.commit()

def temp_exists(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    cur.execute("show tables")
    data = cur.fetchall()
    if "temp_operations" in data:
        return True
    return False

def create_temp(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    c = "create table temp_operations (type varchar(1), translation varchar (10), operation_part_1 varchar(50), operation_part_2 varchar(50))"
    cur.execute(c)
    a = "insert into temp_operations select * from operations"
    cur.execute(a)
    con.commit()

def add_preset(type, part_1, part_2, translation, password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    a = "insert into temp_operations values ( '%s', '%s', '%s', '%s' )" %(type, part_1, part_2, translation)
    cur.execute(a)
    con.commit()

def delete_preset(part_1,part_2, password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    a = "delete from temp_operations where operation_part_1 = '%s' and operation_part_2 = '%s'" %(part_1, part_2)
    cur.execute(a)
    con.commit()

'''
data will be of form
The columns will be Type, Translation, Operation Part 1, Operation Part 2
[("2", "/", "divide","by"), ("2", "*", "multiply","with"), ("2", "*", "multiply","by")...]
'''

def update_dicts(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    a = "select * from temp_operations"
    cur.execute(a)
    global operations
    operations = cur.fetchall()
        
def view_presets(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password)
    cur = con.cursor()
    cur.execute("use alphacalc")
    a = "select * from temp_operations"
    cur.execute(a)
    return cur.fetchall()


def new_temp(password):
    if not temp_exists(password):
        create_temp(password)
    else:
        delete_temp(password)
        create_temp(password)

#search results will also be a list of tuples, like view presets
def search(keyword, password):
    keyword = keyword.lower()
    search_results = []
    list_presets = view_presets(password)
    for tup in list_presets:
        for part in tup:
            if part.lower() == keyword:
                search_results.append(tup)
    for tup in list_presets:
        for part in tup:
            if part.lower() in keyword or keyword in part.lower():
                search_results.append(tup)
    for tup in list_presets:
        for part in tup:
            if len(part) == len(keyword):
                for q in range(len(part)):
                    if (part[0:q] == keyword[0][0:q].lower()) and (part[q+1::].lower() == keyword[0][q+1::]):
                        search_results.append(tup)
    return search_results
