# statmodel.linear_regression

import statsmodels.formula.api as __model

class __result :
    summary = None

def run (a_data,a_feature,a_target) :
    # locals()['x'] = a_feature
    # locals()['y'] = a_target
    loc_model = __model.ols(a_target + " ~ " + a_feature,a_data).fit()
    loc_result = __result()
    loc_result.summary = loc_model.summary()
    return loc_result