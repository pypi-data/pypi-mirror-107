from sklearn.tree import DecisionTreeClassifier as __model
from sklearn.model_selection import GridSearchCV as __gridscv
import sklearn.metrics as __metrics
import pandas as __pd

import anoapycore as __ap

class __result :
    model = None
    evals = None
    best_estimator = None
    best_score = None
    best_params = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x,a_y) :

    loc_parameters = {'max_depth':range(3,20)}

    loc_model = __gridscv(__model(),loc_parameters,n_jobs=-1)
    loc_model.fit(a_x,a_y)
    loc_predict = loc_model.predict(a_x)

    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals = __ap.__eval.evals(a_y.to_numpy(),loc_predict)
    loc_result.best_estimator = loc_model.best_estimator_
    loc_result.best_score = loc_model.best_score_
    loc_result.best_params = loc_model.best_params_
    
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
