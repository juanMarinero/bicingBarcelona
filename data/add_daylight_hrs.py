import numpy as np
import pandas as pd

from datetime import datetime


def hours_of_daylight(date, axis=23.44, latitude=41.39):
    """Compute the hours of daylight for the given date"""
    # http://mathforum.org/library/drmath/view/56478.html formula "D = 24 - (24/pi) [...]"
    #  days = (date - pd.datetime(2000, 12, 21)).days # see default file in get_data()
    days = (date - datetime(2000, 12, 21)).days  # see default file in get_data()
    m = 1.0 - np.tan(np.radians(latitude)) * np.tan(
        np.radians(axis) * np.cos(days * 2 * np.pi / 365.25)
    )
    return 24.0 * np.degrees(np.arccos(1 - np.clip(m, 0, 2))) / 180.0


def add_daylight_hrs(data):
    """Add the daylight_hrs for the location and time period of the default file in get_data() (i.e. location: Barcelona; timelapse: December(aprox))
    Parameters
    ----------
    data : pandas.DataFrame data from function get_data()
    Returns
    -------
    data : with new daylight_hrs column
    """

    origIndex = data.index
    data.index = origIndex.floor("D")

    daysArr = list(set(data.index))
    daylight_hrs = pd.Series(
        list(map(hours_of_daylight, daysArr)), index=daysArr, name="daylight_hrs"
    ).sort_index()
    data = data.join(daylight_hrs)

    import inspect  # get functions name

    if data["daylight_hrs"].isnull().values.any():
        print(f"Missing daylight hours. Function: {inspect.stack()[0][3]}")

    data.index = origIndex

    if 0:
        plt.plot(daylight_hrs)
        plt.plot(data.index, data["daylight_hrs"].values)

    return data
