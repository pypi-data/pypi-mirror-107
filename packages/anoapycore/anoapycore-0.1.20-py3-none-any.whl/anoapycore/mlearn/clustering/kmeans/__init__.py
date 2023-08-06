# ml

import numpy as __np
import pandas as __pd
from sklearn.cluster import KMeans as __model
from kneed import KneeLocator as __find_k
import matplotlib.pyplot as __plt
from mpl_toolkits import mplot3d as __plt3d
from IPython import get_ipython as __ipython

class __result :
    columns = None # list of __columns
    optimum_k = None
    sse = None # sum of the squared errors
    __clusters = None
    clusters = None
    __centroids = None
    centroids = None
    elbow_chart = None
    __prediction = None # prediction in array format
    prediction = None # the cluster by model
    __label = [] # filtered label of clusters
    worksheet = None # features data and the cluster by model

def run (a_data,a_features,a_max_clusters_to_try=11) :
    
    # find optimum k
    loc_sse = []
    for k in range(1,a_max_clusters_to_try):
        loc_model = __model(n_clusters=k)
        loc_model.fit(a_data[a_features])
        loc_sse.append(loc_model.inertia_)
    loc_find_k = __find_k(range(1,a_max_clusters_to_try),loc_sse,curve="convex",direction="decreasing")
    loc_optimum_k = loc_find_k.elbow
    
    # run model with optimum k
    loc_model = __model(n_clusters=loc_optimum_k)
    loc_model.fit(a_data[a_features])
    
    # predict the labels of clusters.
    loc___prediction = loc_model.fit_predict(a_data[a_features])
    loc_prediction = __pd.DataFrame(loc___prediction,columns=['__cluster'])
    loc_label = []
    loc_merge = __pd.merge(a_data,loc_prediction,left_index=True,right_index=True)
    
    # clusters
    loc_clusters = __np.unique(loc___prediction)
    loc_new_data = a_data[a_features]
    for i in loc_clusters :
        loc_label.insert(i,loc_new_data[loc___prediction == i])
        
    # elbow chart
    loc_elbow_chart = __elbow_chart(a_max_clusters_to_try,loc_sse)
    
    # get result
    loc_result = __result()
    loc_result.columns = a_features
    loc_result.optimum_k = loc_optimum_k
    loc_result.sse = loc_sse
    loc_result.__clusters = loc_clusters
    loc_result.clusters = __pd.DataFrame(loc_clusters,columns=['Cluster'])
    loc_result.__centroids = loc_model.cluster_centers_
    loc_result.centroids = __pd.DataFrame(loc_model.cluster_centers_,columns=a_features)
    loc_result.elbow_chart = loc_elbow_chart 
    loc_result.__prediction = loc___prediction
    loc_result.prediction = loc_prediction
    loc_result.__label = loc_label
    loc_result.worksheet = loc_merge

    # final
    return loc_result
    
def __elbow_chart (a_max_clusters_to_try,a_sse) :
    loc_plot = __plt.figure()
    __plt.style.use("fivethirtyeight")
    __plt.plot(range(1,a_max_clusters_to_try),a_sse)
    __plt.xticks(range(1,a_max_clusters_to_try))
    __plt.xlabel("Number of Clusters")
    __plt.ylabel("SSE")
    __plt.close()
    return loc_plot
    
def plot (a_model,a_column_x,a_column_y) :    
    __plt.xlabel(a_column_x)
    __plt.ylabel(a_column_y)
    for i in a_model.__clusters :
        __plt.scatter(a_model.__label[i][:][a_column_x],a_model.__label[i][:][a_column_y],label=i)
        __plt.scatter(a_model.__centroids[i][:][a_model.columns.index(a_column_x)], \
            a_model.__centroids[i][:][a_model.columns.index(a_column_y)], s = 80, color = 'black')
    __plt.legend()
    __plt.show()    

def plots (a_model) :    
    for loc_column_x in a_model.columns :
        for loc_column_y in a_model.columns :
            if loc_column_x != loc_column_y :
                plot(a_model,loc_column_x,loc_column_y)

def plot3d (a_model,a_column_x,a_column_y,a_column_z) :    
    __ipython().run_line_magic('matplotlib', 'notebook') # %matplotlib notebook
    loc_fig = __plt.figure()
    loc_ax = loc_fig.add_subplot(111,projection='3d')
    for i in a_model.__clusters :
        loc_ax.scatter(a_model.__label[i][:][a_column_x],a_model.__label[i][:][a_column_y], \
            a_model.__label[i][:][a_column_z],label=i,cmap='Set2')
        loc_ax.scatter(a_model.__centroids[i][:][a_model.columns.index(a_column_x)],a_model.__centroids[i][:][a_model.columns.index(a_column_y)], \
            a_model.__centroids[i][:][a_model.columns.index(a_column_z)],cmap='Set2',s=80,color='black')
    loc_ax.legend()
    loc_ax.set_xlabel(a_column_x)
    loc_ax.set_ylabel(a_column_y)
    loc_ax.set_zlabel(a_column_z)
    __plt.show()    

