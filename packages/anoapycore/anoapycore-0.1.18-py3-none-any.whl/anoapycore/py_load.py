import pandas as __pd
import .py_data as data

def csv (a_filename) :
    return __pd.read_csv(a_filename)    

def text (a_filename,a_separator=',') :
    return __pd.read_csv(a_filename,a_separator)    

