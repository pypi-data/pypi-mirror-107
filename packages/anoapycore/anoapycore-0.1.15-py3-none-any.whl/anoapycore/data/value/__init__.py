import pandas as __pd

def one_hot_encoding (a_data) :
    """
    Set one hot encoding for unique values of the data
    """
    loc_items = unique(a_data)
    loc_item_set = set(loc_items)
    loc_encoded_vals = []
    for loc_index, loc_row in a_data.iterrows():
        loc_row_set = set(loc_row) 
        loc_labels = {}
        loc_uncommons = list(loc_item_set - loc_row_set)
        loc_commons = list(loc_item_set.intersection(loc_row_set))
        for uc in loc_uncommons:
            loc_labels[uc] = 0
        for com in loc_commons:
            loc_labels[com] = 1
        loc_encoded_vals.append(loc_labels)
    loc_encoded_vals[0]
    loc_ohe_df = __pd.DataFrame(loc_encoded_vals)
    return loc_ohe_df

def unique (a_data) :
    """
    Get unique items in the data
    """
    return (a_data['0'].unique())

def top_unique (a_data) :
    #Assign it to a variable and provide column name once the tuble get converted to actual dataframe columns
    loc_unique_df = a_data.apply(lambda x: __top_unique_count(x,a_data)).rename(index={0:"Value",1:'Percentage',2:'Count'}) \
        .T.sort_values(by='Count',ascending=False)
    return loc_unique_df
    
# Create a method that returns a tuple that give information on the top most common value,
# its percentage and count for each feature
def __top_unique_count(x,a_data) :
    unq_cnt = (x.value_counts(ascending=False,dropna=False).head(1).index.values[0],
               100 * x.value_counts(ascending=False,dropna=False).head(1).values[0]/a_data.shape[0],
               x.value_counts(ascending=False,dropna=False).head(1).values[0])
    return unq_cnt    

