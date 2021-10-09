from preset_management import *

create_temp()
add_preset(["like_exp","operations_overall"], "into", "*")
update_dicts()
print(like_exp)

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

print(evaluation("4 into 3 divided by 2"))
