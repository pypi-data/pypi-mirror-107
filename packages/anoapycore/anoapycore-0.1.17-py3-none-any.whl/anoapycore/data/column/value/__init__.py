# data.column.value

from . import null

import numpy as __np

def replace (a_data,a_column,a_old,a_new) :
    loc_new_data = a_data
    # a_data[a_column].replace(a_old,a_new,inplace=True) # before
    loc_new_data[a_column] = loc_new_data[a_column].replace(a_old,a_new,inplace=False)
    return loc_new_data

def replaces (a_data,a_column,a_old,a_new) :
    loc_new_data = a_data
    loc_new_data[a_column] = loc_new_data[a_column].replace([a_old],a_new,inplace=False)
    return loc_new_data

def unique (a_data,a_column) :
    return list(__np.unique(a_data[a_column]))
