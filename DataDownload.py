import pandas as pd
import json
import glob
import os
import pandas as pd

folder_patch = r"C:\Users\Medion\Desktop\Dane\"

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
print(df.head())
df.to_csv("zebrane_dane.csv", index=False)