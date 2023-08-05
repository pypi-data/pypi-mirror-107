import numpy as __np

def null (a_dataframe) :
    return a_dataframe.isnull().sum()
    
def unique (a_dataframe,a_column) :
    return list(__np.unique(a_dataframe[a_column]))
