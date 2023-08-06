import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt
import pandas as __pd

import anoapycore as __ap

class __result :
    model = None
    evals = {}
    report = None
    roc_chart = None

class __result_predict :
    probability = None
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def __run (a_model,a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5) :
    # loc_model = __model(solver=b_solver,max_iter=b_max_iter) # load library
    
    loc_model = a_model
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
    
    # false positive rate, true positive rate
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test, loc_model.predict_proba(a_x_test)[:,1])
    loc_roc_chart = __roc(a_y_test,loc_predic_test,loc_fpr,loc_tpr)
    
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __ap.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __ap.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report # print(report)
    loc_result.roc_chart = loc_roc_chart # roc_chart.show()
    return loc_result

def __roc (a_y_test,a_y_pred,a_fpr,a_tpr) :
    loc_logit_roc_auc = __metrics.roc_auc_score(a_y_test,a_y_pred)
    loc_plot = __plt.figure()
    __plt.plot(a_fpr,a_tpr,label='Area = %0.2f' % loc_logit_roc_auc)
    __plt.plot([0, 1], [0, 1],'r--')
    __plt.xlim([0.0, 1.0])
    __plt.ylim([0.0, 1.05])
    __plt.xlabel('False Positive Rate')
    __plt.ylabel('True Positive Rate')
    __plt.title('Receiver Operating Characteristic')
    __plt.legend(loc="lower right")
    __plt.close()
    return loc_plot

def __predict (a_model,a_data,b_features='',b_threshold=0.5) :
    if b_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = b_features
        
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
