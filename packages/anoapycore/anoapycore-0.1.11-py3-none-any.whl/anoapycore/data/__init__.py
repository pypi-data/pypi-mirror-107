from . import column
from . import load
from . import null
from . import row
from . import save
from . import stat
from . import value

import pandas as __pd
from sklearn.preprocessing import MinMaxScaler as __minmax
from sklearn.preprocessing import StandardScaler as __standard

def copy (a_data) :
    """
    This function is aimed to copy one dataframe to another dataframe.
    This will prevent a dataframe to be affected by another dataframe.
    """
    return a_data.copy()

def dimension (a_dataframe) :
    print (str(row.count(a_dataframe)) + ' rows x ' + str(column.count(a_dataframe)) + ' columns')
       
def sample (a_data,a_row=5) :
    return a_data.head(a_row)

def info (a_data) :
    return a_data.info()
    
def merge (a_data_1,a_data_2) :
    """
    Merge 2 dataframes by index
    """
    loc_new_df = __pd.merge(a_data_1,a_data_2,left_index=True,right_index=True)
    return loc_new_df

def normalize (a_data,a_column,b_method='MinMax') :
    """
    This function is aimed to normalize data.
    Use [] when passing parameter to a_column.
    Options for b_method = 'MinMax' (default),'Standard'
    Return directly to a_data[a_column]
    """
    if b_method == 'MinMax' :
        loc_scaler = __minmax()
        a_data[a_column] = loc_scaler.fit_transform(a_data[a_column])
    elif b_method == 'Standard' :
        loc_scaler = __standard()
        a_data[a_column] = loc_scaler.fit_transform(a_data[a_column])
        
def map (a_data,a_column,a_old,a_new) :
    """
    Map value a_old of a_column in a_data with a_new
    Use [] in a_old and a_new
    a_new must match in length with a_old
    """
    loc_new_data = a_data
    a_data[a_column].replace(a_old,a_new,inplace=True)

def unique (a_data,a_column) :
    """
    Get unique value of a_column in a_data (for int or float data type only)
    """
    return list(__np.unique(a_data[a_column]))
        
def select (a_data,a_column) :
    """
    Select a_column in a_data
    Use [] in a_column
    """
    return a_data[a_column]
        
def deselect (a_data,a_column) :
    """
    Not to select a_column in a_data
    Get remaining columns
    Use [] in a_column
    """
    loc_data = a_data.drop(a_column,axis = 1)    
    return loc_data

