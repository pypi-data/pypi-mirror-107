# chart.pairplot

import matplotlib.pyplot as __plt
import seaborn as __sns
import multipledispatch as __dispatch

def show (a_data) :
    __sns.pairplot(a_data)

def shows (a_data,a_columns) :
    __sns.pairplot(a_data[a_columns])
