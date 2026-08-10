import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dtale

array = np.load(r"C:\Users\brand\Downloads\responses_211022.npy")

print(array)
df = pd.DataFrame(array)

print(df)

d = dtale.show(df)

# Print the access link
print(f"Access D-Tale here: {d.main_url}")
