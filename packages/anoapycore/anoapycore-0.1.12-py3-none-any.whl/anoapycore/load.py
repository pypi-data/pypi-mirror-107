import pandas as __pd
from .data import *

def csv (a_filename) :
    return __pd.read_csv(a_filename)    

def text (a_filename,a_separator=',') :
    return __pd.read_csv(a_filename,a_separator)    

