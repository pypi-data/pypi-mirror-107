# chart.boxplot

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data,a_column) :
    return __sns.boxplot(x=a_data[a_column])

def shows (a_data,a_column_x,a_column_y) :
    return __sns.boxplot(data=a_data,x=a_column_x,y=a_column_y)
    
