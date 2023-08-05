from .value import *

def count (a_dataframe) :
    return len(a_dataframe.columns)    
    
def delete (a_dataframe,a_column) :
    loc_dataframe = a_dataframe.drop([a_column], axis = 1)    
    return loc_dataframe

def delete (a_dataframe,a_column) :
    loc_dataframe = a_dataframe.drop(a_column, axis = 1)    
    return loc_dataframe
    
def list_ (a_dataframe) :
    return list(a_dataframe)
    
def select (a_dataframe,a_column) :
    return a_dataframe[a_column]
