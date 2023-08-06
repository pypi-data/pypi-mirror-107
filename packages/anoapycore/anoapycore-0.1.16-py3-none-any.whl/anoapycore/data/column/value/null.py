# data.column.value.null

import numpy as __np

def count (a_data) :
    return a_data.isnull().sum()
    
def replace (a_data,a_column,a_method='mean') :
    if a_method == 'mean' :
        return a_data[a_column].fillna(a_data[a_column].mean(),inplace=True)
    
def replace_text (a_data,a_column,a_text) :
    a_data[a_column].replace(a_text,__np.nan,inplace=True)
    return a_data[a_column].fillna(a_data[a_column].mode()[0],inplace=True)
