def desc (a_data) :
    return a_data.describe()
    
def mean (a_data) :
    return a_data.mean()

def mean_ (a_data,a_groupby) :
    return a_data.groupby(a_groupby).mean()
    
def median (a_data) :
    return a_data.median()