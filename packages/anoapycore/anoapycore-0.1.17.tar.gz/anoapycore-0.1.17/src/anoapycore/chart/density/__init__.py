"""
A density plot is a smoothed, continuous version of a histogram estimated from the data. 
The most common form of estimation is known as kernel density estimation. 
In this method, a continuous curve (the kernel) is drawn at every individual data point 
and all of these curves are then added together to make a single smooth density estimation. 
The kernel most often used is a Gaussian (which produces a Gaussian bell curve at each data point).
"""

# chart.density

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data,a_column,a_fill=False) :
    return __sns.kdeplot(a_data[a_column],shade=a_fill)

def shows (a_data,a_columns,a_fill=False) :
    loc_fig = __plt.figure()
    for i in a_columns:
        __sns.kdeplot(a_data[i],shade=a_fill)
    loc_fig.legend(labels=a_columns,bbox_to_anchor=(1.01,1),loc=2)
    __plt.close()
    return loc_fig
