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
from imblearn.over_sampling import SMOTE as __smote

import anoapycore as __ap

def array_to_df (a_array) :
    return __pd.DataFrame(a_array)

def copy (a_data) :
    """
    This function is aimed to copy one dataframe to another dataframe.
    This will prevent a dataframe to be affected by another dataframe.
    """
    return a_data.copy()

def df_to_array (a_data) :
    return a_data.to_numpy()

def deselect (a_data,a_column) :
    """
    Not to select a_column in a_data
    Get remaining columns
    Use [] in a_column
    """
    loc_data = a_data.drop(a_column,axis = 1)    
    return loc_data

def dimension (a_data) :
    print (str(row.count(a_data)) + ' rows x ' + str(column.count(a_data)) + ' columns')
    
def groupby (a_data,a_column,b_method='count') :
    if b_method == 'count' :
        loc_result = a_data.groupby(a_column).count() 
    elif b_method == 'mean' :
        loc_result = a_data.groupby(a_column).mean() 
    return loc_result
    # for future dev : 
    # from collections import Counter
    # print(sorted(Counter(a_data[a_column]).items()))
    
def info (a_data) :
    return a_data.info()
    
def map (a_data,a_column,a_old,a_new) :
    """
    Map value a_old of a_column in a_data with a_new
    Use [] in a_old and a_new
    a_new must match in length with a_old
    """
    loc_new_data = a_data
    a_data[a_column].replace(a_old,a_new,inplace=True)

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
        
def unique (a_data,a_column) :
    """
    Get unique value of a_column in a_data (for int or float data type only)
    """
    return list(__np.unique(a_data[a_column]))
        
def sample (a_data,a_row=5) :
    return a_data.head(a_row)

def select (a_data,a_column) :
    """
    Select a_column in a_data
    Use [] in a_column
    """
    return a_data[a_column]
        
def select_by_value (a_data,a_value) :
    return a_data.loc[a_data[a_column] == a_value]
        
def smote (a_x,a_y) :
    loc_smote = __smote()
    loc_x = __ap.data.df_to_array(a_x)
    loc_y = __ap.data.df_to_array(a_y)
    loc_x_smote,loc_y_smote = loc_smote.fit_resample(loc_x,loc_y)
    loc_x_smote = __ap.data.array_to_df(loc_x_smote)
    loc_y_smote = __ap.data.array_to_df(loc_y_smote)
    return loc_x_smote,loc_y_smote
        
