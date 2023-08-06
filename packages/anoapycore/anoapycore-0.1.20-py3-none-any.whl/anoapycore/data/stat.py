import multipledispatch as __dispatch

def desc (a_data) :
    return a_data.describe()
    
@__dispatch.dispatch(object)
def mean (a_data) :
    return a_data.mean()

@__dispatch.dispatch(object,str)
def mean (a_data,a_groupby) :
    return a_data.groupby(a_groupby).mean()
    
def median (a_data) :
    return a_data.median()