from os import path

import pandas as pd

from definitions import const, helpers


class _Statistics:
    def __init__(self, name):
        self.pickle = path.join(const.data_dir, f"{name}.pkl")

    def _create_pickle(self):
        pd.DataFrame([]).to_pickle(self.pickle)

    def _get_dataframe(self) -> pd.DataFrame:
        if not path.exists(self.pickle):
            self._create_pickle()

        return pd.read_pickle(self.pickle)

    def add_stat(self, size: int, time: int):
        dataframe = self._get_dataframe().append([[size, round(time)]])
        dataframe.to_pickle(self.pickle)

    def print_stat(self):
        if self._get_dataframe().empty:
            print("Insufficient Data")
            return

        size_total = int(self._get_dataframe()[0].sum())
        time_total = int(self._get_dataframe()[1].sum())
        average = round(time_total / size_total)

        print(self._get_dataframe())
        print(f"Total Size: {size_total}")
        print(f"Total Length: {time_total}")
        print(f"Average: {average} s/GB")

    def estimate(self, size: int):
        if self._get_dataframe().empty:
            return "Insufficient Data"

        size_total = int(self._get_dataframe()[0].sum())
        time_total = int(self._get_dataframe()[1].sum())
        average = round(time_total / size_total)
        return helpers.format_time(size * average)


compression = _Statistics("compression")
upload = _Statistics("upload")
