# ml

from mlxtend.frequent_patterns import apriori as __model
from mlxtend.frequent_patterns import association_rules as __rules

class __result :
    freq_items = None
    rules = None
    worksheet = None

def run (a_data,b_min_support=0.5,b_min_confidence=0.5) :
    loc_freq_items = __model(a_data,min_support=b_min_support,use_colnames=True,max_len=None,verbose=1,low_memory=False)
    loc_rules = __rules(loc_freq_items,metric="confidence",min_threshold=b_min_confidence,support_only=False)
    # get result
    loc_result = __result()
    loc_result.freq_items = loc_freq_items
    loc_result.rules = loc_rules
    loc_result.worksheet = loc_rules
    return loc_result
