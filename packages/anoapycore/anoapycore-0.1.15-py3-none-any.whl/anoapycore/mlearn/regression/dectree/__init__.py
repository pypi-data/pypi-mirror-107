import pandas as __pd
import numpy as __np
from sklearn.tree import DecisionTreeRegressor as __model
from sklearn.metrics import mean_squared_error as __mse

class __result :
    model = None
    r_square = None # coefficient of determination

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_data,a_feature,a_target) :
    loc_feature = a_data[a_feature]
    loc_target = a_data[a_target]
    loc_model = __model()
    loc_model.fit(loc_feature,loc_target) # create a model
    loc_y_pred = loc_model.predict(loc_feature)
    loc_mse = __mse(loc_target,loc_y_pred)
    loc_rmse = __np.sqrt(loc_mse)
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.r_square = loc_model.score(loc_feature,loc_target)
    return loc_result

def predict (a_model,a_data,a_features='') :
    if a_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = a_features
    loc_prediction = __pd.DataFrame(a_model.model.predict(a_data[loc_features]),columns=['__pred_y'])
    loc_merge = __pd.merge(a_data,loc_prediction,left_index=True,right_index=True)
    loc_result_predict = __result_predict()
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    return loc_result_predict