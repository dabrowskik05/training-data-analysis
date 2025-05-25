# %%
import pandas as pd
import json
import glob
import os
import numpy as np

# %%
folder_patch = "pdu-2025L-dane-json/"

json_files = glob.glob(os.path.join(folder_patch, "*.json"))

data = []

for file in json_files:
    with open(file, "r", encoding='utf-8') as f:
        try:
            record = json.load(f)
            data.append(record)
        except json.JSONDecodeError:
            print(f"Blad w dekodowaniu w pliku: {file}")

df = pd.DataFrame(data)
df = df.dropna(axis=1, how="all")
columns_to_drop = [
    col for col in df.columns if df[col].apply(lambda x: x == df[col].iloc[0]).all()
]
df.drop(columns=columns_to_drop, inplace=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.loc[:, 'session_id'] = np.arange(len(df.iloc[:, 0]))

df = df.sort_values('timestamp').reset_index(drop=True)
df.to_csv("zebrane_dane_json.csv", index=False)

# %%
