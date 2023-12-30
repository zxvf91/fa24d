import numpy as np

import pandas as pd


def kpa_to_psi(kpa: float):
    return kpa*0.1456038

def c_to_f(c: float):
    return c*1.8+32

def compute_lap_times(df: pd.DataFrame,
                      lap_num_col: str = 'lap_number',
                      time_col: str = 'elapsed_time') -> dict:
    
    return (df.groupby(lap_num_col)[time_col].max() - df.groupby(lap_num_col)[time_col].min()).to_dict()    