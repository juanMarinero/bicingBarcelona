import pandas as pd


def add_weather(data,w):
    """Add the weather dataframe from get_weather() to the bicing dataframe from get_data().
    Parameters
    ----------
    data : pandas.DataFrame data from function get_data()
    w:     pandas.DataFrame data from function get_weather()
    Returns
    -------
    data : with new weathers columns
    """
    
    origIndex = data.index
    data.index = origIndex.floor('H')
    
    w.index = w.index.floor('H')
    w = w[~w.index.duplicated(keep='first')]
    
    #data = data.join(w)
    data = pd.merge(data,w,left_index=True,right_index=True, how='left')
    
    data.index = origIndex
    
    return data;
