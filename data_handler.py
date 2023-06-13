import os
import pandas as pd
import numpy as np
import datetime


class DataHandler():
    def __init__(self, sample_file):
        self.file_location = os.path.join(
            os.path.dirname(__file__), 'data', sample_file)
        self.data = None
        self._load_file()

    def _load_file(self):
        self.data = pd.read_excel(self.file_location)

    def get_averages(self):
        duration = self.data['duration'].values

        if len(duration) == 0:
            average_list = []
        elif len(duration) <= 8:
            average_list = duration
        else:
            split_list = np.array_split(duration, 8)
            average_list = [np.average(split) for split in split_list]

        average_list.sort()
        print('Previous durations: {}'.format(average_list))
        return average_list

    def save_time(self, duration):
        duration_s = pd.Series(
            [20, datetime.datetime.now(), duration], index=self.data.columns)
        added_duration_df = pd.concat(
            [self.data, duration_s.to_frame().T], ignore_index=True)
        with pd.ExcelWriter(self.file_location) as writer:
            added_duration_df.to_excel(
                writer, sheet_name='Sheet1', index=False)
