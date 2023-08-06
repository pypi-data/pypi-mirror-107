# ml

import sklearn.linear_model as __model

class __result :
    coefficient = None
    intercept = None

def run (a_data,a_feature,a_target) :
    loc_feature = a_data[a_feature]
    loc_target = a_data[a_target]
    loc_model = __model.LinearRegression() # load library
    loc_model.fit(loc_feature,loc_target) # create a model
    loc_result = __result()
    loc_result.coefficient = loc_model.coef_
    loc_result.intercept = loc_model.intercept_
    return loc_result

