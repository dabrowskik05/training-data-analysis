# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, os.path
import glob
import json
# %%
path = "pdu-2025L-dane-json/"

json_files = glob.glob(os.path.join(path, "*.json"))

data = []

for file in json_files:
    with open(file, "r", encoding='utf-8') as f:
        try:
            record = json.load(f)
            data.append(record)
        except json.JSONDecodeError:
            print(f"Blad w dekodowaniu w pliku: {file}")

df = pd.DataFrame(data)
# %%
