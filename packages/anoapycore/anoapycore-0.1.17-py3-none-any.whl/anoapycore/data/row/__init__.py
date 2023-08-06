def count (a_data) :
    return len(a_data)    
    
# check if there are duplicated rows
def duplicate (a_data) :
    return a_data.duplicated(keep=False).sum()    