import os
from urllib.request import urlretrieve

import pandas as pd

# http://opendata-ajuntament.barcelona.cat/data/es/dataset/bicing
BICING_URL = "opendata-ajuntament.barcelona.cat/data/dataset/fa94d2f3-3428-47b8-9f2b-f1e4423e745a/resource/33bb617f-dc02-48a5-a2ac-fcf6ab4d54cd/download"


def get_data(filename = "biciBcn201812.csv", url=BICING_URL,
                     force_download=False):
    """Download and cache the fremont data
    Parameters
    ----------
    filename : string (optional)
        location to save the data
    url : string (optional)
        web location of the data
    force_download : bool (optional)
        if True, force redownload of data
    Returns
    -------
    data : pandas.DataFrame
        The bicing data from Barcelona
    """
    if force_download or not os.path.exists(filename):
        urlretrieve(url, filename)
    data = pd.read_csv(filename, keep_default_na=False, index_col="updateTime")

    try:
        data.index = pd.to_datetime(data.index, format='%d/%m/%y %H:%M:%S')
    except TypeError:
        data.index = pd.to_datetime(data.index)

    return data
