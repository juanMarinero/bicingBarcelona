import pandas as pd

import holidays as vacations

def add_holidays(data):
    """Add the holidays of 2018 in Barcelona as a column of dataframe data from function get_data().
    Parameters
    ----------
    data : pandas.DataFrame data from function get_data()
    Returns
    -------
    data : with new holiday column
    """
    
    holidays = pd.DatetimeIndex([*vacations.ES(prov='CAT', years=2018)])

    origIndex = data.index
    data.index = origIndex.floor('D')
    
    data = data.join(pd.Series(1, index=holidays, name='holiday'))
    data['holiday'].fillna(0, inplace=True)
    
    data.index = origIndex
    
    # check 
    if 0:
        print(any(data['holiday']==1))
        print(data.iloc[690000,:]) # 2018-12-06 is a holiday in Bcn
        data.loc[690000,'holiday']
    
    return data;
