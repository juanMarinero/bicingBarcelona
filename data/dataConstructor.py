import pandas as pd
from data.data import get_data

from sklearn.preprocessing import LabelEncoder

from data.add_weather import add_weather
from data.add_holidays import add_holidays
from data.add_daylight_hrs import add_daylight_hrs

from data.weather import get_weather


def dataConstructor(data=get_data(), w=get_weather()):
    """Add the weather's, holidays and daylight hours varaibles to the bicing dataframe from get_data().
    Parameters
    ----------
    data : pandas.DataFrame data from function get_data()
    Returns
    -------
    data : with new columns
    """

    data = add_holidays(data)
    data = add_daylight_hrs(data)
    data = add_weather(data, w)

    smallDataFrames = False
    if smallDataFrames:
        # https://www.reddit.com/r/learnpython/comments/5err0o/memoryerror_merging_two_dataframes_with_pandas/
        # MemoryError merging two dataframes with pandas will happen in line: X = X.join(pd.get_dummies(data[k]))
        # Therefore, just skip indeces
        data["day_of_week"] = data.index.day_name()
        data["hour"] = data.index.hour
    else:
        data.reset_index(level=0, inplace=True)
        data["day_of_week"] = data.loc[:, "updateTime"].dt.day_name()
        data["hour"] = data.loc[:, "updateTime"].dt.hour
        try:
            data.drop(columns=["updateTime"], inplace=True)
        except Exception as err:
            print(f"\tError: {err}" + "\n" + 80 * "~")

    boolVars = ["status", "type"]
    dummyVars = ["day_of_week"]

    X = data.drop(
        columns=[
            *boolVars,
            *dummyVars,
            "latitude",
            "longitude",
            "nearbyStations",
            "streetName",
            "streetNumber",
        ]
    )  # .copy()

    for k in boolVars:
        X[k] = LabelEncoder().fit_transform(data[k].values)
    for k in dummyVars:
        X = X.join(pd.get_dummies(data[k]))

    if 0:
        X.rename(
            columns={
                "Monday": "Day1",
                "Tuesday": "Day2",
                "Wednesday": "Day3",
                "Thursday": "Day4",
                "Friday": "Day5",
                "Saturday": "Day6",
                "Sunday": "Day7",
            },
            inplace=True,
        )

    return X
