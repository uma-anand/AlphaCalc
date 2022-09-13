from preset_management import view_presets
from math import *


#calculates expression given the input multiply 3 by 4 or 
 
def translate_operations(phrase,password):
    op = view_presets(password)
    for a in op:
        if a[2] in phrase and a[3] in phrase:
            operation = a
            break
    else:
        return phrase
    if operation[0] not in " ":
        sub_ind = phrase.index(operation[3])
    operation_ind = phrase.index(operation[2])
    if operation[0] == "2":
        to_eval = phrase[operation_ind+len(operation[2]):sub_ind:]+operation[1]+phrase[sub_ind+len(operation[3])::]
    elif operation[0] == "1":
        to_eval = phrase[sub_ind+len(operation[3])::]+operation[1]+phrase[operation_ind+len(operation[2]):sub_ind:]
    elif operation[0] == "" or operation[0] == " ":
        to_eval = phrase[:operation_ind:]+operation[1]+phrase[operation_ind+len(operation[2])::]
    elif operation[0] == "3":
         to_eval = '('+phrase[:operation_ind:]+operation[1]+'('+phrase[operation_ind+len(operation[2])::]+'))'
    try:
        return str(eval(to_eval))
    except Exception:
        return to_eval
 
 # split the expression into smaller fragments based on bracket placements

def split_expression(expression,password):
    from re import split
    fragments=list(filter(None,split(r'[()]',expression)))
    translated=[]
    for x in fragments:
        try:
            translated+=[translate_operations(x,password)]
        except Exception:
            translated+=[x]
    ans=''
    for x,y in zip(fragments,translated):
        ans=expression.replace(x,y)
        expression=ans
    if ans.find('('):
        remove_brackets = list(filter(None,split(r'[()]',ans)))
        ans = ''
        for x in remove_brackets:
            ans+=x
    try:
        return eval(str(ans))
    except Exception:
        return split_expression(ans,password)

#if brackets not already added, adds them mechanically, from left to right

def addbrackets(express,password):
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
    new_expression = str(eval(translate_operations(expression[:second_char:],password)))+expression[second_char::]
    try:
        return split_expression(new_expression,password)
    except SyntaxError:
        return addbrackets(new_expression,password)

# control of evaluation

def evaluation(expression,password):
    try:
        return split_expression(expression,password)
    except SyntaxError:
        return addbrackets(expression,password)

#end
