import sklearn.model_selection as __sklearn

def split (feature,label,train_size=0.70) :
    x_train,x_test,y_train,y_test = __sklearn.train_test_split(feature,label,test_size=1-train_size,random_state=0)
    return x_train,x_test,y_train,y_test
