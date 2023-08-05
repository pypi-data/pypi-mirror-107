import colorama
 

def count(text):
    colorama.init(autoreset=True)
    pystatistic_end = 0
    dic={'letter':0,'integer':0,'space':0,'other':0}
    for i in text:
        if i >'a' and i<'z' or i>'A' and i<'Z' :
            dic['letter'] +=1
        elif i in '0123456789':
            dic['integer'] +=1
        elif i ==' ':
            dic['space'] +=1
        else:
            dic['other'] +=1
    try:
        pystatistic_mode + "1"
    except NameError as e:
        pystatistic_mode = "normal"
    if pystatistic_mode == "normal":
        pystatistic_end = 1
        return dic
    if pystatistic_mode == "print":
        pystatistic_end = 1
        print(dic)
    if pystatistic != 1:
        print("\033[0;31m%s\033[0m" % "Error 961:Wrong mode")
