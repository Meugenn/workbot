def fuzzy_search(string1, string2):
#String1 - name of task; String2 - input string; Returns True, if strings are similar, else False
    count = 0
    for symbol1 in string1.lower():
        for symbol2 in string2.lower():
            if symbol1 == symbol2:
                count += 1
    if (count / len(string2)) > 0.8:
        return True
    else:
        return False   
           