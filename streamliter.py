# %%
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
# %%
path1 = "zebrane_dane_y.csv"
path2 = "zebrane_dane_X.csv"
X = pd.read_csv(path2)
y = pd.read_csv(path1)
# %%
X = X[["total_movements", "active_time[s]", "training_effect", "lap_count", "distance[km]"]]
X["active_time[s]"] = X["active_time[s]"]/60
X.columns = ["total_movements", "active_time[min]", "training_effect", "lap_count", "distance[km]"]
# %%
model = RandomForestRegressor(n_estimators=500,max_depth=20, random_state=42, n_jobs=-1)
model.fit(X, y)
# %%
import streamlit as st
st.title("Predykcja spalonych kalorii")
total_movements = st.number_input("liczba pełnych kroków/obrotów", min_value=0.0)
active_time = st.number_input("aktywny czas [min]", min_value=0.0)
training_effect = st.number_input("efekt treningowy (0-5)", min_value=0, max_value=5)
lap_count = st.number_input("liczba serii", min_value=1)
distance = st.number_input("pokonany dystans [km]", min_value=0.0)

if st.button("Przewidź kalorie"):
    X_input = np.array([[total_movements, active_time, training_effect, lap_count, distance]])
    prediction = model.predict(X_input)[0]
    st.write(f"Spalone kalorie: {prediction:.2f} kcal")
# %%

