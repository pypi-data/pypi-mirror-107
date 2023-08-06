from .load import *
from .column import *
from .row import *

class params :
    filename = ''

class c_data :

    column = c_column()

    def describe (a_dataframe) :
        print ('Column Count : ' + str(column.count(a_dataframe)))
        print ('Row Count : ' + str(row.count(a_dataframe)))
    
    def descriptive (a_params) :
        loc_data = load.csv(a_params.filename)
        describe (loc_data)

