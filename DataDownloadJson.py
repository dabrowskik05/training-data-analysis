# %%
import pandas as pd
import json
import glob
import os
import numpy as np

# %%
folder_path = "C:\\Users\\szymo\\Desktop\\pdu-2025L-dane-json"

json_files = glob.glob(os.path.join(folder_path, "*.json"))

data = []

for file in json_files:
    with open(file, "r", encoding='utf-8') as f:
        record = json.load(f)
        data.append(record)


df = pd.DataFrame(data)

# %%
df = df.dropna(axis=1, how="all")
columns_to_drop = [
    col for col in df.columns if df[col].apply(lambda x: x == df[col].iloc[0]).all()
]
df.drop(columns=columns_to_drop, inplace=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df.sort_values('timestamp').reset_index(drop=True)
df.loc[:, 'session_id'] = np.arange(len(df.iloc[:, 0]))

df.to_csv("zebrane_dane_json.csv", index=False)

# %%
