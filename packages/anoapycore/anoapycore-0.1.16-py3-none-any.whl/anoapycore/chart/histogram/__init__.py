# chart.histogram

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data,a_column,a_bins='auto',a_color='#0504aa',a_alpha=0.7,a_grid_y=True) :
    __plt.hist(x=a_data[a_column],bins=a_bins,color=a_color,alpha=a_alpha)
    __plt.title(a_column)
    __plt.xlabel('Value')
    __plt.ylabel('Frequency')
    if a_grid_y == True :
        __plt.grid(axis='y',alpha=0.7)
    __plt.show()
    
