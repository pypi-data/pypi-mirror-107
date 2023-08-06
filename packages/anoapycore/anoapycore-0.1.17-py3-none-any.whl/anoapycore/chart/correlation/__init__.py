# chart.correlation

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data) :
    """
    Correlation plot
    """
    loc_corr = a_data.corr()
    return __sns.heatmap(loc_corr, cmap = 'Wistia', annot= True);