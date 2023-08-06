import sklearn.linear_model as __log_reg
import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt
import pandas as __pd

class __result :
    model = None
    accuracy_train = None
    accuracy_test = None
    report = None
    roc_chart = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x_train,a_x_test,a_y_train,a_y_test,b_solver='lbfgs',b_max_iter=1000) :
    loc_model = __log_reg.LogisticRegression(solver=b_solver,max_iter=b_max_iter) # load library
    loc_model.fit(a_x_train,a_y_train) # create a model
    
    loc_accuracy_train = loc_model.score(a_x_train,a_y_train) 
    loc_accuracy_test = loc_model.score(a_x_test,a_y_test) 
    # predictor.score(X,Y) internally calculates Y'=predictor.predict(X) and then compares Y' against Y to give an accuracy measure
    
    loc_prediction = loc_model.predict(a_x_test) # prediction of y by the model
    loc_report = __metrics.classification_report(a_y_test,loc_prediction)
    
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test, loc_model.predict_proba(a_x_test)[:,1])
    # false positive rate, true positive rate
    
    loc_roc_chart = __roc(a_y_test,loc_prediction,loc_fpr,loc_tpr)
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.accuracy_train = loc_accuracy_train
    loc_result.accuracy_test = loc_accuracy_test
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
