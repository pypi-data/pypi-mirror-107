# ml

import sklearn.linear_model as __log_reg
import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt

class __result :
    model = None
    accuracy = None
    report = None
    y_pred = None
    roc_chart = None

def run (a_x_train,a_x_test,a_y_train,a_y_test) :
    loc_model = __log_reg.LogisticRegression() # load library
    loc_model.fit(a_x_train,a_y_train) # create a model
    
    loc_accuracy = loc_model.score(a_x_test,a_y_test) 
    # predictor.score(X,Y) internally calculates Y'=predictor.predict(X) and then compares Y' against Y to give an accuracy measure
    
    loc_y_pred = loc_model.predict(a_x_test) # prediction of y by the model
    loc_report = __metrics.classification_report(a_y_test,loc_y_pred)
    
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test, loc_model.predict_proba(a_x_test)[:,1])
    # false positive rate, true positive rate
    
    loc_roc_chart = __roc(a_y_test,loc_y_pred,loc_fpr,loc_tpr)
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.accuracy = loc_accuracy
    loc_result.y_pred = loc_y_pred
    loc_result.report = loc_report # print(report)
    loc_result.roc_chart = loc_roc_chart # roc_chart.show()
    return loc_result

def __roc (a_y_test,a_y_pred,a_fpr,a_tpr) :
    loc_logit_roc_auc = __metrics.roc_auc_score(a_y_test,a_y_pred)
    loc_plot = __plt.figure()
    __plt.plot(a_fpr,a_tpr,label='Logistic Regression (Area = %0.2f)' % loc_logit_roc_auc)
    __plt.plot([0, 1], [0, 1],'r--')
    __plt.xlim([0.0, 1.0])
    __plt.ylim([0.0, 1.05])
    __plt.xlabel('False Positive Rate')
    __plt.ylabel('True Positive Rate')
    __plt.title('Receiver Operating Characteristic')
    __plt.legend(loc="lower right")
    __plt.close()
    return loc_plot

