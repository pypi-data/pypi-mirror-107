import pickle as __pkl

def load (a_file) :
    return __pkl.load(open(a_file,'rb'))

def save (a_model,a_file) :
    __pkl.dump(a_model,open(a_file,'wb'))
