import pandas as __pd

def csv (a_filename) :
    return __pd.read_csv(a_filename)    

def text (a_filename,a_separator=',') :
    return __pd.read_csv(a_filename,a_separator)    

