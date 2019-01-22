import os
from urllib.request import urlretrieve

import pandas as pd

# https://rp5.ru/Weather_archive_in_Barcelona_(airport),_METAR
WEATHER_URL = "http://37.200.66.117/download/files.metar/LE/LEBL.30.11.2018.31.12.2018.1.0.0.en.utf8.00000000.xls.gz"

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
        urlretrieve(url, filename)
    w = pd.read_excel(filename)


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
                        'c':'Clouds',
                        'VV':'Visibility',
                        'WW':'Rain/...'
                       }, inplace = True)
    w.drop(columns=['DD', 'P0', 'P','ff10', "W'W'", 'Td'], inplace=True)

    # modify columns
    w['Visibility'].replace('10.0 and more', 10, inplace=True)
    w['Clouds'] = [c.split()[0] for c in w['Clouds'].astype(str)]
    w['Clouds'].replace(['Broken', 'Few', 'No', 'Scattered'], [75, 20, 0, 45], inplace=True)

    w['Rain/...'].fillna('No rain', inplace=True)
    w = w.join(pd.get_dummies(w['Rain/...']))
    w.drop(columns=['Rain/...'], inplace=True)

    # check
    if 0:
        w.Visibility.plot(); plt.show()
        w.Clouds.plot(); plt.show()
        w[['°C']].plot(); plt.show()

    return w;
