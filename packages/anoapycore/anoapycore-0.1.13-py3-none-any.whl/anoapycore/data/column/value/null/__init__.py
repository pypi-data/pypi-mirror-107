import numpy as __np

def count (a_data,a_column) :
    return a_data[a_column].isnull().sum()

def replace (a_data,a_column,b_method='mean') :
    if b_method == 'mean' :
        a_data[a_column].fillna(a_data[a_column].mean(),inplace=True) # before
    
def replace_text (a_data,a_column,a_text,b_method='mode') :
    a_data[a_column].replace(a_text,__np.nan,inplace=True)
    return a_data[a_column].fillna(a_data[a_column].mode()[0],inplace=True)
