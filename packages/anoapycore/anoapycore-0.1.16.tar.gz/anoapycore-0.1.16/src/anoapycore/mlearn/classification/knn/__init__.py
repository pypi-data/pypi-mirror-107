from sklearn.neighbors import KNeighborsClassifier as __model
import sklearn.metrics as __metrics
import pandas as __pd

import anoapycore as __ap

class __result :
    model = None
    evals = {}
    report = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x_train,a_x_test,a_y_train,a_y_test) :

    loc_model = __model(n_neighbors=3)
    loc_model.fit(a_x_train,a_y_train)
    
    loc_predic_train = loc_model.predict(a_x_train)
    loc_predic_test = loc_model.predict(a_x_test)
    
    loc_report = __metrics.classification_report(a_y_test,loc_predic_test)

    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __ap.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __ap.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report # print(report)
    
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
