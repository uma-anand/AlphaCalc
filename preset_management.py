from start_up import *

def add_preset(type, part_1, part_2, translation, password):
    if type == '':
        type = ' '
    elif part_2 == '':
        part_2 = ' '
    con = ms.connect(host = "localhost", user = "root", passwd = password,database = 'alphacalc')
    cur = con.cursor()
    a = "insert into operations values ( '%s', '%s', '%s', '%s' )" %(type,translation, part_1, part_2)
    cur.execute(a)
    con.commit()

def delete_preset(part_1,part_2, password):
    con = ms.connect(host = "localhost", user = "root", passwd = password,database = 'alphacalc')
    cur = con.cursor()
    a = "delete from operations where operation_part_1 = '%s' and operation_part_2 = '%s'" %(part_1, part_2)
    cur.execute(a)
    con.commit()

'''
data will be of form
The columns will be Type, Translation, Operation Part 1, Operation Part 2
[("2", "/", "divide","by"), ("2", "*", "multiply","with"), ("2", "*", "multiply","by")...]
'''

        
def view_presets(password):
    con = ms.connect(host = "localhost", user = "root", passwd = password,database = 'alphacalc')
    cur = con.cursor()
    a = "select * from operations"
    cur.execute(a)
    return cur.fetchall()


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
