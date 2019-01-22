import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from sklearn.decomposition import PCA


def cumuExplVariance(X):
    """np.cumsum(pca.explained_variance_ratio_)
    Parameters
    ----------
    X : dataFrame equivalent to X, from dividing matrix data in X(n_samples,m_features) and y(n_samples,1_feature)
    Returns
    -------
    None
    """

    pca = PCA().fit(X)

    plt.plot(np.cumsum(pca.explained_variance_ratio_), '*-')
    plt.xlabel('number of components', fontsize=18)
    plt.ylabel('cumulative explained variance', fontsize=18);
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    
    return;
