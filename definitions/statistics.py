from os import path

import pandas as pd

from definitions import const, helpers


def _create_pickle():
    pd.DataFrame([]).to_pickle(const.stats_pickle)


def _get_dataframe() -> pd.DataFrame:
    if not path.exists(const.stats_pickle):
        _create_pickle()

    return pd.read_pickle(const.stats_pickle)


def add_stat(size: int, time: int):
    dataframe = _get_dataframe().append([[size, time]])
    dataframe.to_pickle(const.stats_pickle)


def print_stat():
    if _get_dataframe().empty:
        print("Insufficient Data")
        return

    size_total = int(_get_dataframe()[0].sum())
    time_total = int(_get_dataframe()[1].sum())
    average = round(time_total / size_total)

    print(_get_dataframe())
    print(f"Total Size: {size_total}")
    print(f"Total Length: {time_total}")
    print(f"Average: {average} s/GB")


def estimate(size: int):
    if _get_dataframe().empty:
        return "Insufficient Data"

    size_total = int(_get_dataframe()[0].sum())
    time_total = int(_get_dataframe()[1].sum())
    average = round(time_total / size_total)
    return helpers.format_time(size * average)
