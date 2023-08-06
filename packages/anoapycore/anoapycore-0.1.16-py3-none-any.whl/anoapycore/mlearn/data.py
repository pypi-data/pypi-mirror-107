import sklearn.model_selection as __sklearn

class result :
    x_train = None
    x_test = None
    y_train = None
    y_test = None

def split (a_feature,a_label,a_train_size=0.70) :
    loc_result = result()    
    loc_result.x_train,loc_result.x_test,loc_result.y_train,loc_result.y_test = __sklearn.train_test_split(a_feature,a_label,test_size=1-a_train_size,random_state=0)
    return loc_result
