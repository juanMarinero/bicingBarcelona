import os
from urllib.request import urlretrieve

import numpy as np
import pandas as pd

# https://rp5.ru/Weather_archive_in_Barcelona_(airport),_METAR
# WEATHER_URL = "http://37.200.66.117/download/files.metar/LE/LEBL.30.11.2018.31.12.2018.1.0.0.en.utf8.00000000.xls.gz"
WEATHER_URL = "https://ru5.rp5.ru/download/files.synop/81/8181.30.11.2018.31.12.2018.1.0.0.en.utf8.00000000.xls.gz"

def get_weather(filename = "LEBL.30.11.2018.31.12.2018.1.0.0.en.utf8.00000000.xls", url=WEATHER_URL,
                     force_download=False):
    """Download the weather data from Barcelona (default in December)
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
        The weather data from Barcelona
    """
    if force_download or not os.path.exists(filename):
        download_file = filename + ".gz"
        urlretrieve(url, download_file)
        
        import gzip
        with gzip.open(download_file, 'r') as f:
            df = pd.read_excel(f)
            df.to_excel(filename)
    w = pd.read_excel(filename)
    w = w.iloc[:,1:] # delete col

    # header
    headerRow = 5
    w.columns = w.iloc[headerRow] # set header
    w.columns.name = ''
    w = w.iloc[(headerRow+1):,:] # delete rows previous to header

    # index
    try:
        w.index = pd.to_datetime(w.iloc[:,0], format='%d.%m.%Y %H:%M')
    except TypeError:
        w.index = pd.to_datetime(w.index)
    w = w.iloc[:,1:] # delete col

    # select columns
    w.rename(columns = {'U':'Humidity (%)', 
                        'T':'°C', 
                        'Ff':'Wind (m/s)', 
                        'N':'Clouds',
                        'VV':'Visibility',
                        'WW':'Rain/...'
                       }, inplace = True)
    cols = set(['Humidity (%)', '°C', 'Wind (m/s)', 'Clouds', 'Visibility', 'Rain/...'])
    w.drop(columns=set(w.columns).difference(cols), inplace=True)
    print(w.columns) # debug

    # modify columns
    w['Visibility'].replace('10.0 and more', 10, inplace=True)
    w['Clouds'] = [c.split()[0] for c in w['Clouds'].astype(str)]
    # print(set(w['Clouds'])) # debug
    mask = np.array(w['Clouds']=="100%", dtype=bool)
    w['Clouds'][mask] = 100
    w['Clouds'][~mask] = [int(c[:2]) if c[:2].isnumeric() and int(c[:2]) in range(0,99) else 0 for c in w['Clouds'][~mask]]
    # print(set(w['Clouds'])) # debug
    # w['Clouds'].replace(['Broken', 'Few', 'No', 'Scattered'], [75, 20, 0, 45], inplace=True) # 2019 table

    rain_nan = "No significant weather observed. "
    w['Rain/...'].fillna(rain_nan, inplace=True)
    w['Rain/...'][w['Rain/...']==" "] = rain_nan
    w = w.join(pd.get_dummies(w['Rain/...']))
    w.drop(columns=['Rain/...'], inplace=True)
    
    w.fillna(0) # all NaN to 0

    # check
    if 0:
        w.Visibility.plot(); plt.show()
        w.Clouds.plot(); plt.show()
        w[['°C']].plot(); plt.show()

    return w;

# +
# get_weather().head(10)
# get_weather().columns
# get_weather()['Clouds'].head(10)
# -


