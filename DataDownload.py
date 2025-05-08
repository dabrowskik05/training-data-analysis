import pandas as pd
import json
import glob
import os

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

print(df.head())
df.to_csv("zebrane_dane.csv", index=False)