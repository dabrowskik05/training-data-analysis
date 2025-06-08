# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %%
path = "zebrane_dane.csv"
df = pd.read_csv(path)
# %%
new_column_names = ["end_datetime","start_datetime","start_latitude[°]","start_longitude[°]",
    "elapsed_time[s]","active_time[s]","distance[km]","total_strokes[strokes]","nec_latitude[°]",
    "nec_longitude[°]","swc_latitude[°]","swc_longitude[°]","avg_speed_enhanced[km/h]",
    "max_speed_enhanced[km/h]","calories[kcal]","avg_speed_basic[km/h]","max_speed_basic[km/h]",
    "total_ascent[m]","total_descent[m]","lap_count","vertical_oscillation[mm]","stance_time_pct[%]",
    "stance_time[ms]","vertical_ratio[%]","stance_balance[%]","step_length[mm]","sport","sub_sport",
    "avg_hr[bpm]","max_hr[bpm]","avg_cadence[rpm]","max_cadence[rpm]","training_effect",
    "avg_temperature[°C]","max_temperature[°C]","avg_cadence_fractional[rpm]","max_cadence_fractional[rpm]",
    "anaerobic_effect","fractional_ascent[m]","fractional_descent[m]","total_strides[strides]",
    "avg_run_cadence[strides/min]","max_run_cadence[strides/min]","total_cycles[cycles]"]
df.columns = new_column_names
# %% sprawdzamy podstawy
print(df.shape)
print(df.dtypes)
print(df.describe())
print(len(df.columns))
df.isna().sum()
# %%
df.loc[:,"calories[kcal]"].sum()
# %%
df.start_datetime = pd.to_datetime(df.loc[:,"start_datetime"])
df.end_datetime = pd.to_datetime(df.loc[:,"end_datetime"])
df.loc[:,"duration"] = (df.end_datetime - df.start_datetime).dt.total_seconds()
df = df.sort_values("start_datetime")
# %% o co chodzi XD
(df.loc[:,"elapsed_time[s]"] - df.loc[:,"duration"]).describe() 
# wartości z przedziału (-1860, -4) - duration dłuższe od elapsed i active_time
# %%
(df["active_time[s]"] > df["elapsed_time[s]"]).sum() # 0, czyli elapsed to z przerwami
df.loc[:,"pause_time[s]"] = df.loc[:,"elapsed_time[s]"] - df.loc[:,"active_time[s]"]
df.loc[:,"pause_time[s]"].describe()
# %% policzyłem duration wiec nie ma co trzymać dat i godzin, lokalizacja niepotrzebna do kalorii
df = df.drop(['end_datetime', 'start_datetime', 'start_latitude[°]','start_longitude[°]',
         'nec_latitude[°]','nec_longitude[°]','swc_latitude[°]', 'swc_longitude[°]'], axis=1)
# %%
(df.loc[:,'avg_speed_basic[km/h]'] - df.loc[:,"avg_speed_enhanced[km/h]"]).dropna(how='all').sum() # 0
(df.loc[:,'max_speed_basic[km/h]'] - df.loc[:,"max_speed_enhanced[km/h]"]).dropna(how='all').sum() # 0
# prędkość basic i enhanced są równe, wiec wywalam basic
df = df.drop(['avg_speed_basic[km/h]','max_speed_basic[km/h]'], axis=1)
# %% sprawdzam czy można obliczyć predkość z pozostałych kolumn
speed_delta = df.loc[:,"distance[km]"]*3600/df.loc[:,"active_time[s]"] - (df.loc[:,"avg_speed_enhanced[km/h]"])
speed_delta.describe() # maksymalna różnica to blisko 0.002 km/h
df.loc[:,"avg_speed_enhanced[km/h]"].isna().sum()/len(df)
# usuwamy prędkość - dużo braków (81%), a można obliczyć
df = df.drop("avg_speed_enhanced[km/h]", axis=1)
# %%
df.loc[:,['vertical_oscillation[mm]','stance_time_pct[%]','stance_time[ms]', 
          'vertical_ratio[%]','stance_balance[%]', 'step_length[mm]']].isna().sum()/len(df)
#około 90% wartości jest NAN więc te 6 kolumn ma zbyt dużo braków
df = df.drop(['vertical_oscillation[mm]','stance_time_pct[%]','stance_time[ms]',
            'vertical_ratio[%]','stance_balance[%]', 'step_length[mm]'], axis=1)
# %% 
df.loc[:,"elapsed_time[s]"].isna().sum() # elapsed_time jest bez wartości NA
sporty = df.groupby(["sport","sub_sport"])
sporty["elapsed_time[s]"].count()
# sport-odnotowania: cycling-816, hiking-81, running-289, gen_running-289, trail_running-458, walking-91
sporty[["avg_run_cadence[strides/min]","avg_cadence[rpm]"]].apply(lambda x: x.isna().sum())
# kolumna "avg_run_cadence[strides/min]" jest dla running, "avg_cadence[rpm]" dla pozostałych
# połączmy je
df.loc[:,"avg_cadence[rpm/spm]"] = np.where(
    df.loc[:,"sport"] == "running",
    df.loc[:,"avg_run_cadence[strides/min]"],
    df.loc[:,"avg_cadence[rpm]"])
# analogicznie:
sporty[["max_run_cadence[strides/min]","max_cadence[rpm]"]].apply(lambda x: x.isna().sum())
df.loc[:,"max_cadence[rpm/spm]"] = np.where(
    df.loc[:,"sport"] == "running",
    df.loc[:,"max_run_cadence[strides/min]"],
    df.loc[:,"max_cadence[rpm]"])
df = df.drop(['avg_cadence[rpm]', 'max_cadence[rpm]','avg_run_cadence[strides/min]','max_run_cadence[strides/min]'], axis=1)
# %%
df.loc[:,["avg_cadence[rpm/spm]","avg_cadence_fractional[rpm]"]].describe()
# general_avg_cadence - wartości całkowite w przedziale [7,103]
# avg_cadence_fractional - wartości ułamkowe w przedziale [0,1) - część ułamkowa?
df.loc[:,"avg_cadence[rpm/spm]"] = df.loc[:,"avg_cadence[rpm/spm]"] + df.loc[:,"avg_cadence_fractional[rpm]"]
df.loc[:,"max_cadence[rpm/spm]"] = df.loc[:,"max_cadence[rpm/spm]"] + df.loc[:,"max_cadence_fractional[rpm]"]
df = df.drop(["avg_cadence_fractional[rpm]", "max_cadence_fractional[rpm]"], axis=1)
# %% analogicznie dla ascent/descent
df.loc[:, ["total_ascent[m]","fractional_ascent[m]"]].describe()
df.loc[:,"total_ascent[m]"] =df.loc[:, "total_ascent[m]"] + df.loc[:,"fractional_ascent[m]"].fillna(0)
df.loc[:,"total_descent[m]"] =df.loc[:, "total_descent[m]"] + df.loc[:,"fractional_descent[m]"].fillna(0)
df = df.drop(["fractional_descent[m]","fractional_ascent[m]"], axis=1)
# %%
sporty[["total_strides[strides]","total_strokes[strokes]","total_cycles[cycles]"]].count()
# strikes jest tylko dla running i walking, strokes dla cycling, cycles dla hiking - połączmy je!
df.loc[:,"total_movements"] = df.loc[:,"total_strides[strides]"].fillna(
    df.loc[:,"total_strokes[strokes]"]).fillna(df.loc[:,"total_cycles[cycles]"])
df = df.drop(["total_strides[strides]", "total_strokes[strokes]","total_cycles[cycles]"], axis=1)
# %%
df.loc[:,"move_distance"] = (df.loc[:,"distance[km]"]*1000/df.loc[:,"total_movements"])
sporty = df.groupby(["sport","sub_sport"])
sporty["move_distance"].mean() # więc 1 movement to pełny krok/obrót pedałów
df.loc[:,["move_distance", "calories[kcal]"]].corr() # <0.06
df = df.drop("move_distance", axis=1)
# %% macierz korelacji
correlation_matrix = df.corr(numeric_only=True)
sns.heatmap(correlation_matrix, cmap='coolwarm')
plt.title("Macierz korelacji")
plt.show()
# posortowane korelacje z calories
calories_corr = pd.DataFrame(correlation_matrix.loc[:,"calories[kcal]"]
                             .abs().sort_values(ascending = False)).iloc[1:,:]
print(calories_corr)
# %%
df.isna().sum() # max_speed ma około 80% braków, a do tego korelację tylko 0.41
# pause_time ma bardzo niską korelację, wywalamy oba
df = df.drop(["max_speed_enhanced[km/h]","pause_time[s]"], axis=1)
# %%
df.loc[:,"lap_count"].describe() # ilość "serii"
# %%
df.isna().sum() # NA tylko dla avg_cadence, max_cadence i movements po 231
# %%
# dla Random forest nie trzeba wypełniać NANów, ale porównałem i po wypełnieniu jest lepiej
df.loc[:,"distance_bin"] = pd.qcut(df.loc[:,"distance[km]"], q=5)
df.loc[:,"avg_cadence[rpm/spm]"] = df.groupby(["sport","sub_sport", "distance_bin"]
)["avg_cadence[rpm/spm]"].transform(lambda x: x.fillna(x.median())).sort_index()

df.loc[:,"max_cadence[rpm/spm]"] = df.groupby(["sport","sub_sport", "distance_bin"]
)["max_cadence[rpm/spm]"].transform(lambda x: x.fillna(x.median())).sort_index()

df.loc[:,"total_movements"] = df.groupby(["sport","sub_sport", "distance_bin"]
)["total_movements"].transform(lambda x: x.fillna(x.median())).sort_index()
df = df.drop(columns=["distance_bin"])
# %%
# usuwamy outlinery
d1 = df.drop(["sport","sub_sport"], axis=1)
Q1 = d1.quantile(0.25)
Q3 = d1.quantile(0.75)
IQR = Q3 - Q1
clean = ((d1 >= (Q1 - 1.5 * IQR)) & (d1 <= (Q3 + 1.5 * IQR))).all(axis=1)
df_clean = df.loc[clean,:].reset_index(drop=True)
df_clean # 1418 wierszy, czyli tylko o 316 mniej
df_clean.loc[:,"sport"].unique()
df_clean.loc[:,"sub_sport"].unique()
# wszystkie sporty dalej są
df = df_clean
# %%
# one-hot-encoding
df = pd.get_dummies(df, columns=["sport","sub_sport"], drop_first=True)
df
# %% dzielimy na 2 zbiory
X = df.drop(columns=["calories[kcal]"])
Y = df["calories[kcal]"]
print("X shape:", X.shape)
print("Y shape:", Y.shape)
# %% sprawdzamy jak tam nasze dane
print(X.columns)
print(Y.describe())
X.head()
# %%
X.to_csv("zebrane_dane_X.csv", index=False)
Y.to_csv("zebrane_dane_Y.csv", index=False)
#koniec cz.1
# %%
df.loc[1234,:]
# %%
