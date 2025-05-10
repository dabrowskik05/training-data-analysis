# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, os.path
import glob
import json
# %%
path = "zebrane_dane.csv"

df = pd.read_csv(path)
df.columns
# %%
df["start_time"] = df["start_time"].str.slice(0, 19)
df["timestamp"] = df["timestamp"].str.slice(0, 19)
# %%
df
# %%
