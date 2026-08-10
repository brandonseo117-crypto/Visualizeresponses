import pandas as pd
import numpy as np
from pathlib import Path

np.set_printoptions(threshold=np.inf)

array = np.load(r"C:\Users\brand\Downloads\V4_tuning_curve_responses\tuning_curve_responses\responses_190923_neuron1.npy")

print(len(array))