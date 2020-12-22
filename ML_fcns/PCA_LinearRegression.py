import pandas as pd
import numpy as np

from IPython.display import display_html
import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")

from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from scipy import stats


def PCA_LinearRegression(
    XdC,
    ydC,
    n_components,
    index,
    just_coef_determination=False,
    display_table_bool=True,
):
    """Apply Principal Component Analysis (PCA) to XdC.values (n_components is the PCA parameter value).
    Parameters
    ----------
    XdC : dataFrame equivalent to X, from dividing matrix data in X(n_samples,m_features) and y(n_samples,1_feature)
        extract it values to apply PCA()
        extract it columns to display pca.components_ dataframe
    ydC : analogous to XdC
        extract y.values to plot agains y_predicted (see Returns)
        to calculate correlation against y_predicted
    n_components : PCA parameter
        PCA parameter
        to build pca.components_'s dataframe index
    index : dates(and time) of XdC and ydC dataframes
        plt.plot(index, y, [...])
        plt.plot(index, y_predicted, [...])
    Returns
    -------
    y_predicted : array
        estimation output from applying LinearRegression() to PCA eigenvectors
    """
    X = XdC.values
    y = ydC.values

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    model = LinearRegression(fit_intercept=True)
    model.fit(X_pca, y)
    y_predicted = model.predict(X_pca)

    # Correlación
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        y[:, 0], y_predicted[:, 0]
    )

    if not just_coef_determination:
        plt.figure(figsize=(20, 5))
        plt.plot(index, y, alpha=0.3, label="data")
        plt.plot(index, y_predicted, alpha=0.3, label="regression")
        plt.legend()
        plt.title(f"R^2 = {100*(r_value**2):.2f} %", fontsize=20)

        if display_table_bool:
            df_coef = pd.DataFrame(
                np.abs(pca.components_),
                index=["PC-" + str(k) for k in range(n_components)],
                columns=XdC.columns,
            )
            display_html(
                df_coef.style.set_caption("pca.components_")
                .background_gradient(axis=1, cmap="Greens")
                .format("{:.0e}")
            )

    return 100 * (r_value ** 2)
