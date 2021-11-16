from preset_management import *

update_dicts()

#calculates expression given the input multiply 3 by 4 or 
 
def translate_operations(phrase):
    for a in operations:
        if a[2] in phrase:
            operation = a
            break
    else:
        return phrase
    if operation[0] != "":
        sub_ind = phrase.index(operation[3])
    operation_ind = phrase.index(operation[2])
    if operation[0] == "2":
        to_eval = phrase[operation_ind+len(operation[2]):sub_ind:]+operation[1]+phrase[sub_ind+len(operation[3])::]
    elif operation[0] == "1":
        to_eval = phrase[sub_ind+len(operation[3])::]+operation[1]+phrase[operation_ind+len(operation[2]):sub_ind:]
    elif operation[0] == "":
        to_eval = phrase[:operation_ind:]+operation[1]+phrase[operation_ind+len(operation[2])::]
    return to_eval
 
# split the expression into smaller fragments based on bracket placements

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

#if brackets not already added, adds them mechanically, from left to right

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

# control of evaluation

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
            pass

