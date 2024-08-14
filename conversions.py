<<<<<<< HEAD
=======
<<<<<<< HEAD
import numpy as np

>>>>>>> 62dcb627f486a3eb5990c39ee417e5f349d9d7b5
def kpa_to_psi(kpa: float) -> float:
    return kpa*0.1456038

def c_to_f(c: float) -> float:
    return c*1.8+32 

def time_string_to_s(time_str: str) -> float:
    minutes, seconds = time_str.split(':')
    return int(minutes) * 60 + float(seconds)

def s_to_time_string(s: float) -> str:
    minutes = int(s // 60)
    seconds = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f'{minutes:2d}:{seconds:02d}.{ms:03d}'

def kpa_to_psi(kpa: float) -> float:
<<<<<<< HEAD
    return kpa*0.1456038
=======
    return kpa*0.1456038
>>>>>>> 62dcb627f486a3eb5990c39ee417e5f349d9d7b5
