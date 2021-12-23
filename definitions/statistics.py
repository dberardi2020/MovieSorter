import pandas as pd

from definitions import const


def clear_dataframe():
    pd.DataFrame([]).to_pickle(const.stats_pickle)


def get_dataframe() -> pd.DataFrame:
    return pd.read_pickle(const.stats_pickle)


def add_stat(size: int, time: int):
    dataframe = get_dataframe().append([[size, time]])
    dataframe.to_pickle(const.stats_pickle)


def read_stat():
    # dataframe = pd.read_pickle(const.stats_pickle)
    print(get_dataframe())
