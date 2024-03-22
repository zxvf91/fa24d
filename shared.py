from dataclasses import dataclass
import pandas as pd
from pandas.core.api import DataFrame
from abc import ABC
import conversions as c

@dataclass
class Session:
    filename: str
    fastest_lap: pd.DataFrame
    laps: list[pd.DataFrame]
    label: str

def downsample(df: pd.DataFrame, *, downsample_factor: int = 1) -> pd.DataFrame:
    return df[::downsample_factor]


class CsvReader(ABC):
    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    def can_read(self) -> bool:
        pass

    def read(self) -> pd.DataFrame:
        pass

class RaceChronoCsvReader(CsvReader):
    column_name_mapping = {
        "lap_number": "Lap Number",
        "latitude": "GPS Latitude",
        "longitude": "GPS Longitude",
        "speed": "GPS Speed",
        "lateral_acc": "GPS LatAcc",
        "accelerator_pos": "PPS",
        "engine_oil_pressure_1": "OilPressure0",
        "rpm": "RPM"
    }

    def can_read(self) -> bool:
        first_line = open(self.filepath).readline()
        return first_line.startswith("This file is created using RaceChrono")
    
    def read(self) -> pd.DataFrame:
        df = pd.read_csv(
            self.filepath, 
            header=0,
            dtype={"lap_number": int},
            index_col=0,
            skiprows=list(range(0, 9)) + [10, 11],
            usecols=["timestamp", "lap_number", "elapsed_time", "latitude", "longitude", "speed", "lateral_acc", "accelerator_pos", "engine_oil_pressure_1", "rpm"]
        )
        df["engine_oil_pressure_1"] = df["engine_oil_pressure_1"].apply(c.kpa_to_psi)
        df["lateral_acc"] = df["lateral_acc"] * -1

        df.index = pd.to_datetime(df.index, unit="s")

        df = df.rename(columns=self.column_name_mapping)

        lap_times = df.groupby('Lap Number')['elapsed_time'].agg(['min', 'max'])
        lap_times['Lap Time'] = lap_times['max'] - lap_times['min']

        df = df.merge(lap_times['Lap Time'], left_on='Lap Number', right_index=True)
        
        df = df[df['Lap Time'] > 30]

        return df


class AimCsvReader(CsvReader):
    def get_lap_metadata(self) -> pd.DataFrame:
        metadata = pd.read_csv(self.filepath, nrows=2, skiprows=11, header=None).transpose()
        metadata.columns = ["marker", "lap_time"]
        metadata = metadata.drop(0)
        
        metadata["marker"] = metadata["marker"].astype(float)
        metadata["lap_time"] = metadata["lap_time"].apply(c.time_string_to_s)

        return metadata

    def can_read(self) -> bool:
        first_line = open(self.filepath).readline()
        return first_line.startswith('"Format","AiM CSV File"')
    
    def read(self) -> DataFrame:
        df = pd.read_csv(
            self.filepath, 
            header=0, 
            skiprows=list(range(0, 13)) + [15], 
            usecols=["Time", "OilPressure0", "PPS", "GPS LatAcc", "RPM", "GPS Latitude", "GPS Longitude"]
        )
        metadata = self.get_lap_metadata()

        # df.index = pd.to_datetime(df.index, unit="s")
        df["elapsed_time"] = df["Time"]
        df.set_index("elapsed_time", inplace=True)
        df.index = pd.to_datetime(df.index, unit="s")

        df["Lap Number"] = 0
        df["Lap Time"] = 0.0

        prev_marker = 0.0
        for row in metadata.itertuples(index=True):
            i = row.Index
            df.loc[(df["Time"] < row.marker) & (df["Time"] >= prev_marker), "Lap Number"] = i - 1
            df.loc[(df["Time"] < row.marker) & (df["Time"] >= prev_marker), "Lap Time"] = row.lap_time
            prev_marker = row.marker

        return df
    
readers = [RaceChronoCsvReader, AimCsvReader]