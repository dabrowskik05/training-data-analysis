# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
# %%
path1 = "zebrane_dane_X.csv"
path2 = "zebrane_dane_Y.csv"
X = pd.read_csv(path1)
Y = pd.read_csv(path2)
# %%
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, max_error,mean_absolute_percentage_error,median_absolute_error
#  dzielimy na model treningowy i testowy
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=2137)
# w treakcie testowania dobrałem najlepsze parametry
forest = RandomForestRegressor(n_estimators=500,max_depth=20, n_jobs=-1,random_state=2137)
# dopasowujemy model
forest.fit(X_train, Y_train)
# %% testujemy
Y_pred = forest.predict(X_test)
print("MAE:", mean_absolute_error(Y_test, Y_pred))
print("RMSE:", root_mean_squared_error(Y_test, Y_pred))
print("R²:", r2_score(Y_test, Y_pred))
# %% Wykres przewidywania vs rzeczywistość
plt.scatter(Y_test, Y_pred, alpha=0.3)
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--')
plt.xlabel("Rzeczywiste kalorie")
plt.ylabel("Przewidywane kalorie")
plt.title("Predykcja vs Rzeczywistość")
plt.grid(True)
plt.show()
# %% lista ważności cech
importances = forest.feature_importances_
f_importances = pd.DataFrame(dict(feature = X.columns,importance = importances))
f_importances.sort_values(by ="importance",ascending=False)
# %% wykres ważności cech
sorted_idx = f_importances["importance"].argsort()
plt.figure(figsize=(10, 7))
plt.barh(f_importances.loc[sorted_idx,"feature"], f_importances.loc[sorted_idx,"importance"], color = "skyblue")
plt.xlabel("Ważność cechy")
plt.title("Ważność cech według Random Forest")
plt.tight_layout()
plt.show()
# %% pierwsze 6 cech tylko ma znaczenie
X = X.loc[:,['lap_count','total_movements','distance[km]','training_effect','active_time[s]','avg_hr[bpm]']]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=42)
forest.fit(X_train,Y_train)
# %% testujemy znowu
print("MAE:", mean_absolute_error(Y_test, Y_pred))
print("RMSE:", root_mean_squared_error(Y_test, Y_pred))
print("R²:", r2_score(Y_test, Y_pred))
# %% inne merryki
print("max error:",  max_error(Y_test, Y_pred))
print("MAPE:", mean_absolute_percentage_error(Y_test, Y_pred))
print("MedianAE:", median_absolute_error(Y_test, Y_pred))
# %%
forest.fit(X,Y)
# %% lista ważności cech znowu, delikatne różnice
importances = forest.feature_importances_
f_importances = pd.DataFrame(dict(feature = X.columns,importance = importances))
f_importances.sort_values(by ="importance",ascending=False).round(3)
# %% wykres ważności cech, znowu
sorted_idx = f_importances["importance"].argsort()
plt.figure(figsize=(10, 7))
plt.barh(f_importances.loc[sorted_idx,"feature"], f_importances.loc[sorted_idx,"importance"], color = "skyblue")
plt.xlabel("Ważność cechy")
plt.title("Ważność cech według Random Forest")
plt.tight_layout()
plt.show()
# %%
Y_test = np.array(Y_test).reshape(284)
results = pd.DataFrame(dict(prediction = np.array(Y_pred), real = Y_test))
results.loc[:,"absolute_error"] = (results.loc[:,"prediction"]-results.loc[:,"real"]).abs()
results.loc[:,"relative_error[%]"] = results.loc[:,"absolute_error"]*100/results.loc[:,"real"]
len(results.loc[results.loc[:,"relative_error[%]"]>10,:])/len(results) # <6%
results.sort_values(by = "relative_error[%]")
# %% Wykres przewidywania vs rzeczywistość
plt.scatter(Y_test, Y_pred, alpha=0.3)
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--')
plt.xlabel("Rzeczywiste kalorie")
plt.ylabel("Przewidywane kalorie")
plt.title("Predykcja vs Rzeczywistość")
plt.grid(True)
plt.show()
# %%
errors = Y_test - Y_pred
plt.figure(figsize=(8, 5))
plt.hist(errors, bins=30, edgecolor='black')
plt.title("Histogram błędów predykcji")
plt.xlabel("Błąd [kcal]")
plt.ylabel("Liczba przypadków")
plt.grid(True)
plt.tight_layout()
plt.show()
# %%
rel_errors = errors*100/Y_test
plt.figure(figsize=(8, 5))
plt.hist(rel_errors, bins=30, edgecolor='black')
plt.title("Histogram względnych błędów predykcji")
plt.xlabel("Względny błąd [%]")
plt.ylabel("Liczba przypadków")
plt.grid(True)
plt.tight_layout()
plt.show()
# %%
from sklearn.inspection import PartialDependenceDisplay
fig, ax = plt.subplots(figsize=(12, 8))
PartialDependenceDisplay.from_estimator(forest, X_train, X.columns, ax=ax)
plt.suptitle("Wykresy zależności cząstkowych dla Random Forest")
plt.tight_layout()
plt.show()
# %%
from sklearn.tree import plot_tree
tree = forest.estimators_[0] # pierwsze drzewo
plt.figure(figsize=(30,15))
plot_tree(tree, feature_names=X.columns, filled=True, max_depth=2)
plt.show()
# %%
