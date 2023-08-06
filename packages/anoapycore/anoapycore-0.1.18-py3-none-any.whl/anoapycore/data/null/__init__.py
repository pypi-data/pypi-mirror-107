import numpy as __np
import pandas as __pd

def count (a_data) :
    """
    Count null in dataframe.
    You can also use a_data[a_column] or a_data[[a_column1,a_column2,...]]
    """
    return a_data.isnull().sum()
    
def fill (a_data,a_columns,b_fill_with='NA') :
    a_data[a_columns] = a_data[a_columns].fillna(b_fill_with)    
    return a_data

# check in any rows had more null than specific number 
# def greater_than (a_data,a_max_null) :
#    return a_data[a_data.isnull().sum(axis=1) > a_max_null]    
    
def percentage (a_data) :
    missing_info = __pd.DataFrame(__np.array(a_data.isnull().sum().sort_values(ascending=False).reset_index())\
                                ,columns=['Columns','Missing_Percentage']).query("Missing_Percentage > 0").set_index('Columns')
    return 100*missing_info/a_data.shape[0]    
    
def replace (a_data,a_column,b_method='mean') :
    """
    Replace null value with another value.
    The options of b_method are 'mean' (default), 'median'.
    This function has no return.
    """
    if b_method == 'mean' :
        a_data[a_column].fillna(a_data[a_column].mean(),inplace=True)
    elif b_method == 'median' :
        a_data[a_column].fillna(a_data[a_column].median(),inplace=True)
    
def replace_text (a_data,a_column,a_text) :
    """
    Replace null value (which stated by string or text) with another value.
    This function has no return.
    """
    a_data[a_column].replace(a_text,__np.nan,inplace=True)
    a_data[a_column].fillna(a_data[a_column].mode()[0],inplace=True)
    
