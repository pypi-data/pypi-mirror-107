import anoapycore as __ap
from sklearn.linear_model import LogisticRegression as __model

def run (a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5,b_solver='lbfgs',b_max_iter=1000) :
    loc_model = __model(solver=b_solver,max_iter=b_max_iter)
    return __ap.mlearn.classification.__template.__run(loc_model,a_x_train=a_x_train,a_x_test=a_x_test,a_y_train=a_y_train,a_y_test=a_y_test,b_threshold=b_threshold)

def predict (a_model,a_data,b_features='',b_threshold=0.5) :
    return __ap.mlearn.classification.__template.__predict(a_model=a_model,a_data=a_data,b_features=b_features,b_threshold=b_threshold)

