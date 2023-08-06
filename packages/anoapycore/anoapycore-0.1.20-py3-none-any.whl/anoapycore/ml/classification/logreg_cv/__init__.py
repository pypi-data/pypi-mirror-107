"""
Logistic Regression with Cross Validation
"""

import numpy as __np
import pandas as __pd
import sklearn.linear_model as __log_reg
from sklearn.model_selection import KFold as __kfold
from sklearn.model_selection import cross_val_score as __cv_score

class __score :
    min = None
    max = None
    mean = None
    std = None

class __result :
    model = None
    accuracy = None
    score = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x,a_y,b_splits=10) :
    """
    Create a Logistic Regression Model using K-Fold Cross Validation
    """
    # prepare the cross-validation procedure
    loc_cv = __kfold(n_splits=b_splits,random_state=1,shuffle=True)
    # create model
    loc_model = __log_reg.LogisticRegression()
    # evaluate model
    loc_scores = __cv_score(loc_model,a_x,a_y,scoring='accuracy',cv=loc_cv,n_jobs=-1)
    loc_accuracy = __np.mean(loc_scores)
    loc_score_minimun = __np.min(loc_scores)
    loc_score_maximum = __np.max(loc_scores)
    loc_score_mean = __np.mean(loc_scores)
    loc_score_std = __np.std(loc_scores)
    # result
    loc_result = __result()
    loc_result.score = __score()
    loc_result.model = loc_model
    loc_result.accuracy = loc_accuracy
    loc_result.score.min = loc_score_minimun
    loc_result.score.max = loc_score_maximum
    loc_result.score.mean = loc_score_mean
    loc_result.score.std = loc_score_std
    return loc_result

def predict (a_model,a_data,a_features='') :
    """
    Predict a target using Logistic Regression Model with K-Fold Cross Validation
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

