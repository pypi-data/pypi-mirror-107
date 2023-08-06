import sklearn.metrics as __metrics

class __result :
    accuracy = None
    precision = None
    recall = None
    all = None

def report (a_accuracy,a_precision,a_recall) :
    """
    Use print() to show the result
    """
    loc_report = ''
    loc_report = loc_report + 'Accuracy : ' + str(a_accuracy)
    loc_report = loc_report + "\n" +'Precision : ' + str(a_precision)
    loc_report = loc_report + "\n" +'Recall : ' + str(a_recall)
    return loc_report

def evals (a_y_true,a_y_pred) :
    loc_result = __result()
    loc_result.accuracy = accuracy (a_y_true,a_y_pred)
    loc_result.precision = precision (a_y_true,a_y_pred)
    loc_result.recall = recall (a_y_true,a_y_pred)
    loc_result.all = report (loc_result.accuracy,loc_result.precision,loc_result.recall)
    return loc_result

def accuracy (a_y_true,a_y_pred) :
    return __metrics.accuracy_score(a_y_true,a_y_pred)
    
def precision (a_y_true,a_y_pred) :
    return __metrics.precision_score(a_y_true,a_y_pred)    
    
def recall (a_y_true,a_y_pred) :
    return __metrics.recall_score(a_y_true,a_y_pred)        