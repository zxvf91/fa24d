<<<<<<< HEAD
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Dict, List

import pandas as pd

=======
from dataclasses import dataclass
import pandas as pd
from pandas.core.api import DataFrame
from abc import ABC
>>>>>>> af8bb48 (update for verus oil pressure video)
import conversions as c

@dataclass
class Session:
    filename: str
    fastest_lap: pd.DataFrame
<<<<<<< HEAD
    laps: List[pd.DataFrame]
    label: str

def downsample(df: pd.DataFrame, *, downsample_factor: int = 1) -> pd.DataFrame:
    df = df.copy()
    return df[::downsample_factor]


class CSVReader(ABC):
    label: str
=======
    laps: list[pd.DataFrame]
    label: str

def downsample(df: pd.DataFrame, *, downsample_factor: int = 1) -> pd.DataFrame:
    return df[::downsample_factor]


class CsvReader(ABC):
    filepath: str
>>>>>>> af8bb48 (update for verus oil pressure video)

    def __init__(self, filepath: str):
        self.filepath = filepath

<<<<<<< HEAD
    @property
    def use_cols(self) -> List[str]:
        return self._use_cols

    @property
    def column_name_mapping(self) -> Dict[str, str]:
        return self._col_name_mapping
    
    def set_cols(self, config_file: str='column_config.json'):
        cols = []
        conf = json.load(open(config_file, 'r'))
        conf = conf[self.label]
        for prop in conf:
            if conf[prop]:
                cols.append(prop)
        self._use_cols = cols

    def set_col_name_mapping(self, config_file: str='column_labels.json'):
        mappings = json.load(open(config_file, 'r'))
        mappings = mappings[self.label]
        # TODO: add check that use cols exists
        self._col_name_mapping = {k: mappings[k] for k in self.use_cols if k in mappings}

    @abstractmethod
    def can_read(self) -> bool:
        pass

    @abstractmethod
    def read(self) -> pd.DataFrame:
        pass


class RaceChronoReader(CSVReader):
    label = "RaceChrono"
=======
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
>>>>>>> af8bb48 (update for verus oil pressure video)

    def can_read(self) -> bool:
        first_line = open(self.filepath).readline()
        return first_line.startswith("This file is created using RaceChrono")
<<<<<<< HEAD

    def read(self) -> pd.DataFrame:
        self.set_cols()
        self.set_col_name_mapping()

        df = pd.read_csv(
            self.filepath,
=======
    
    def read(self) -> pd.DataFrame:
        df = pd.read_csv(
            self.filepath, 
>>>>>>> af8bb48 (update for verus oil pressure video)
            header=0,
            dtype={"lap_number": int},
            index_col=0,
            skiprows=list(range(0, 9)) + [10, 11],
<<<<<<< HEAD
            usecols=self.use_cols #["timestamp", "lap_number", "elapsed_time", "latitude", "longitude", "speed", "lateral_acc", "accelerator_pos", "engine_oil_pressure_1", "rpm"]
        )
        df["engine_oil_pressure_psi"] = df["engine_oil_pressure"].apply(c.kpa_to_psi)
=======
            usecols=["timestamp", "lap_number", "elapsed_time", "latitude", "longitude", "speed", "lateral_acc", "accelerator_pos", "engine_oil_pressure_1", "rpm"]
        )
        df["engine_oil_pressure_1"] = df["engine_oil_pressure_1"].apply(c.kpa_to_psi)
>>>>>>> af8bb48 (update for verus oil pressure video)
        df["lateral_acc"] = df["lateral_acc"] * -1

        df.index = pd.to_datetime(df.index, unit="s")

        df = df.rename(columns=self.column_name_mapping)

<<<<<<< HEAD
        lap_times = df.groupby('Lap Number')['Time'].agg(['min', 'max'])
        lap_times['Lap Time'] = lap_times['max'] - lap_times['min']

        df = df.merge(lap_times['Lap Time'], left_on='Lap Number', right_index=True)

=======
        lap_times = df.groupby('Lap Number')['elapsed_time'].agg(['min', 'max'])
        lap_times['Lap Time'] = lap_times['max'] - lap_times['min']

        df = df.merge(lap_times['Lap Time'], left_on='Lap Number', right_index=True)
        
>>>>>>> af8bb48 (update for verus oil pressure video)
        df = df[df['Lap Time'] > 30]

        return df


<<<<<<< HEAD
class AIMReader(CSVReader):
    label = "AIM"

=======
class AimCsvReader(CsvReader):
>>>>>>> af8bb48 (update for verus oil pressure video)
    def get_lap_metadata(self) -> pd.DataFrame:
        metadata = pd.read_csv(self.filepath, nrows=2, skiprows=11, header=None).transpose()
        metadata.columns = ["marker", "lap_time"]
        metadata = metadata.drop(0)
<<<<<<< HEAD

=======
        
>>>>>>> af8bb48 (update for verus oil pressure video)
        metadata["marker"] = metadata["marker"].astype(float)
        metadata["lap_time"] = metadata["lap_time"].apply(c.time_string_to_s)

        return metadata

    def can_read(self) -> bool:
        first_line = open(self.filepath).readline()
<<<<<<< HEAD
        return first_line.startswith("Format,AIM CSV")

    def read(self) -> pd.DataFrame:
        self.set_cols()
        self.set_col_name_mapping()

        df = pd.read_csv(
            self.filepath,
            header=0,
            # TODO: skiprows should be moved to a conf somewhere
            skiprows=list(range(0, 12)) + [13, 14, 15],
            usecols=self.use_cols #["Time", "OilPressure0", "PPS", "GPS LatAcc", "RPM", "GPS Latitude", "GPS Longitude"]
        )
        #metadata = self.get_lap_metadata()
        df = df.rename(columns=self.column_name_mapping)
        df.set_index("Time", inplace=True)
        df.index = pd.to_datetime(df.index, unit="s")
       
        df["Lap Number"] = 0
        df["Lap Time"] = 0.0

        # prev_marker = 0.0
        # for row in metadata.itertuples(index=True):
        #     i = row.Index
        #     df.loc[(df["Time"] < row.marker) & (df["Time"] >= prev_marker), "Lap Number"] = i - 1
        #     df.loc[(df["Time"] < row.marker) & (df["Time"] >= prev_marker), "Lap Time"] = row.lap_time
        #     prev_marker = row.marker

        return df

readers = [RaceChronoReader, AIMReader]
=======
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
>>>>>>> af8bb48 (update for verus oil pressure video)
