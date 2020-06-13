def isNone(value) :
    if(value is None):
        return True

    if type(value) == str :
        return len(value) == 0

    if type(value) == list :
        return len(value) == 0  

    if type(value) == tuple :
        return len(value) == 0  

    if type(value) == set :
        return len(value) == 0  

    if type(value) == dict :
        return len(value) == 0 

    return False