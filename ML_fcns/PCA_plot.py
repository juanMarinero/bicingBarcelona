import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
plt.style.use('seaborn-whitegrid')

from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from scipy import stats


def PCA_plot(X, y, n_components=2, c=None):
    """plot pca.inverse_transform
    Parameters
    ----------
    X : matrix X, from dividing matrix data in X(n_samples,m_features) and y(n_samples,1_feature)
    y : (see X)
    n_components : PCA parameter
    c : matplotlib color parameter array
    Returns
    -------
    pca : sklearn.decomposition.PCA method
    X_pca :
        X_pca = pca.transform(X)
        X_pca = pca.inverse_transform(X_pca)
    """
    if np.array(c).size: c=y.flatten()
    pca = PCA(n_components)
    X = np.c_[X,y]
    pca.fit(X)
    X_pca = pca.transform(X)
    X_pca = pca.inverse_transform(X_pca) # delete line ???
    
    fig = plt.figure(figsize=(n_components*6,5))
    plotProperties = dict(alpha=0.5, c=c, cmap='viridis')
    if n_components == 2:        
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2, projection='3d')      
        g = ax1.scatter(  X_pca[:, 0], X_pca[:, 1],    **plotProperties); fig.colorbar(g);
        h = ax2.scatter3D(X_pca[:, 0], X_pca[:, 1], y, **plotProperties)      
        for ax in [ax1,ax2]:
            ax.set_xlabel('PCA component 1')
            ax.set_ylabel('PCA component 2')
        ax2.set_zlabel('y')
        ax2.view_init(60, 15)
        
    elif n_components == 1:
        plt.scatter(X_pca[:, 0], y ,**plotProperties)        
        plt.xlabel('PCA component 1')
        plt.ylabel('y') 

    return (pca, X_pca);
