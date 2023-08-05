"""
Logistic Regression with Cross Validation
"""

import numpy as __np
import pandas as __pd
from sklearn.linear_model import LogisticRegressionCV as __logreg_cv
import sklearn.metrics as __metrics

import anoapycore as __ap

class __result :
    model = None
    evals = None
    # report = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x,a_y,b_cv=5,b_max_iter=1000) :
    """
    Create a Logistic Regression Model with Cross Validation
    """

    loc_model = __logreg_cv(cv=b_cv,random_state=0,max_iter=b_max_iter)
    loc_model.fit(a_x,a_y.values.ravel())    
    loc_predict = loc_model.predict(a_x)

    # result
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals = __ap.__eval.evals(a_y.to_numpy(),loc_predict)
    # loc_result.report = __ap.__eval.report(a_y.to_numpy(),loc_predict)

    return loc_result

def predict (a_model,a_data,a_features='') :
    """
    Predict a target using Logistic Regression Model with Cross Validation
    """
    
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

