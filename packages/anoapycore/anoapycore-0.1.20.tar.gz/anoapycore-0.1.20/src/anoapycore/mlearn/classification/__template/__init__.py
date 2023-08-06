import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt
import pandas as __pd
import numpy as __np

import anoapycore as __ap

class __result :
    model = None
    evals = {}
    report = None
    best_threshold = None
    roc_chart = None
    pr_curve = None # precision-recall curve
    prc_best_threshold = None # precision-recall curve threshold
    prc_best_fscore = None

class __result_predict :
    probability = None
    prediction = None
    worksheet = None

def __run (a_model,a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5) :
    
    loc_model = a_model
    loc_model.fit(a_x_train,a_y_train)
       
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

    loc_report = __metrics.classification_report(a_y_test,loc_predic_test)
    
    loc_predict_proba = loc_model.predict_proba(a_x_test)[:,1]
    # calculate roc curves : false positive rate, true positive rate
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test,loc_predict_proba)
    # calculate the g-mean for each threshold
    loc_gmeans = __np.sqrt(loc_tpr * (1-loc_fpr))
    # locate the index of the largest g-mean
    ix = __np.argmax(loc_gmeans)
    loc_best_threshold = loc_thresholds[ix]
    loc_roc_chart = __roc(a_y_test,loc_predic_test,loc_fpr,loc_tpr,ix)
    
    # calculate prc (precision-recall curve)
    loc_precision,loc_recall,loc_thresholds = __metrics.precision_recall_curve(a_y_test,loc_predict_proba)
    # convert to f score
    loc_fscore = (2 * loc_precision * loc_recall) / (loc_precision + loc_recall)
    # locate the index of the largest f score
    ix = __np.argmax(loc_fscore)
    loc_prc_best_threshold = loc_thresholds[ix]
    loc_best_fscore = loc_fscore[ix]
    loc_pr_curve = __precision_recall_curve(loc_precision,loc_recall,ix)
    
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __ap.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __ap.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report
    loc_result.best_threshold = loc_best_threshold
    loc_result.roc_chart = loc_roc_chart
    loc_result.pr_curve = loc_pr_curve
    loc_result.prc_best_threshold = loc_prc_best_threshold
    loc_result.prc_best_fscore = loc_best_fscore
    return loc_result

def __roc (a_y_test,a_y_pred,a_fpr,a_tpr,a_ix) :
    loc_logit_roc_auc = __metrics.roc_auc_score(a_y_test,a_y_pred)
    loc_plot = __plt.figure()
    __plt.plot(a_fpr,a_tpr,label='Area = %0.2f' % loc_logit_roc_auc)
    __plt.plot([0, 1], [0, 1],'r--')
    __plt.scatter(a_fpr[a_ix],a_tpr[a_ix],marker='o',color='black',label='Best')
    __plt.xlim([0.0, 1.0])
    __plt.ylim([0.0, 1.05])
    __plt.xlabel('False Positive Rate')
    __plt.ylabel('True Positive Rate')
    __plt.title('Receiver Operating Characteristic')
    __plt.legend(loc="lower right")
    __plt.close()
    return loc_plot

def __precision_recall_curve (a_precision,a_recall,a_ix) :
    loc_plot = __plt.figure()
    __plt.plot(a_recall,a_precision,marker='.',label='Plot')
    __plt.scatter(a_recall[a_ix],a_recall[a_ix],marker='o',color='black',label='Best')
    __plt.xlabel('Recall')
    __plt.ylabel('Precision')
    __plt.title('Precision-Recall Curve')
    __plt.legend(loc="upper right")
    __plt.close()
    return loc_plot

def __predict (a_model,a_data,b_features='',b_threshold=0.5) :
    if b_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = b_features
        
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

    loc_result_predict = __result_predict()
    loc_result_predict.probability = loc_probability
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    return loc_result_predict
