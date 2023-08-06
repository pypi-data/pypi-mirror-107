import py_load as load
import py_column as column
import py_row as row

class params :
    filename = ''

def describe (a_dataframe) :
    print ('Column Count : ' + str(column.count(a_dataframe)))
    print ('Row Count : ' + str(row.count(a_dataframe)))
    
def descriptive (a_params) :
    loc_data = load.csv(a_params.filename)
    describe (loc_data)

