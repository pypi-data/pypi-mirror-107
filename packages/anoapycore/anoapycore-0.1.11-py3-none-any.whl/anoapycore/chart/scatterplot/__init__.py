# chart.scatterplot

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data,a_column_x,a_column_y,a_column_by="") :
    """
    Draw a scatterplot
    """
    __sns.set_theme() # apply the default theme
    if a_column_by == "" :
        loc_result = __sns.lmplot(data=a_data,x=a_column_x,y=a_column_y)
    else :
        loc_result = __sns.lmplot(data=a_data,x=a_column_x,y=a_column_y,col=a_column_by)
    return loc_result

