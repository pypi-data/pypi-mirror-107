import anoapycore as __ap
from sklearn.ensemble import GradientBoostingClassifier as __model

def run (a_x_train,a_x_test,a_y_train,a_y_test,b_n_estimators=100,b_learning_rate=1.0,b_max_depth=1,b_threshold=0.5) :
    loc_model = __model(n_estimators=b_n_estimators,learning_rate=b_learning_rate,max_depth=b_max_depth,random_state=0)
    return __ap.mlearn.classification.__template.__run(loc_model,a_x_train=a_x_train,a_x_test=a_x_test,a_y_train=a_y_train,a_y_test=a_y_test,b_threshold=b_threshold)

def predict (a_model,a_data,b_features='',b_threshold=0.5) :
    return __ap.mlearn.classification.__template.__predict(a_model=a_model,a_data=a_data,b_features=b_features,b_threshold=b_threshold)


'''


from sklearn.ensemble import GradientBoostingClassifier as __model
import sklearn.metrics as __metrics
import pandas as __pd

import anoapycore as __ap

class __result :
    model = None
    evals = {}
    report = None

class __result_predict :
    probability = None
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x_train,a_x_test,a_y_train,a_y_test,b_estimators=100,b_learning_rate=1.0,b_max_depth=1,b_threshold=0.5) :

    loc_model = __model(n_estimators=b_estimators,learning_rate=b_learning_rate,max_depth=b_max_depth,random_state=0)
    loc_model.fit(a_x_train,a_y_train)

    # 0.1.19 begin
    
    loc_prob_train = loc_model.predict_proba(a_x_train)[:,1]
    if b_threshold == 0.5 :
        loc_predic_train = loc_model.predict(a_x_train)
    else :
        loc_predic_train = (loc_prob_train >= b_threshold).astype(int)

    loc_prob_test = loc_model.predict_proba(a_x_test)[:,1]
    if b_threshold == 0.5 :
        loc_predic_test = loc_model.predict(a_x_test)
    else :
        loc_predic_test = (loc_prob_test >= b_threshold).astype(int)

    # loc_predic_train = loc_model.predict(a_x_train)
    # loc_predic_test = loc_model.predict(a_x_test)
    
    # 0.1.19 end
        
    loc_report = __metrics.classification_report(a_y_test,loc_predic_test)

    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __ap.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __ap.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report # print(report)
    
    return loc_result

def predict (a_model,a_data,a_features='',b_threshold=0.5) :

    if a_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = a_features
        
    # 0.1.19 begin

    loc_prob_y = a_model.model.predict_proba(a_data[loc_features])[:,1]
    if b_threshold == 0.5 :
        loc_pred_y = a_model.model.predict(a_data[loc_features])
    else :
        loc_pred_y = (loc_prob_y >= b_threshold).astype(int)
        
    loc_probability = __pd.DataFrame(loc_prob_y,columns=['__prob_y'])
    loc_prediction = __pd.DataFrame(loc_pred_y,columns=['__pred_y'])
    
    loc_merge = a_data
    loc_merge = __pd.merge(loc_merge,loc_probability,left_index=True,right_index=True)
    loc_merge = __pd.merge(loc_merge,loc_prediction,left_index=True,right_index=True)

    # 0.1.19 end

    loc_result_predict = __result_predict()
    loc_result_predict.probability = loc_probability
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    
    return loc_result_predict
'''