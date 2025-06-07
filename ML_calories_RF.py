# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
# %%
path1 = "zebrane_dane_X.csv"
path2 = "zebrane_dane_y.csv"
X = pd.read_csv(path1)
y = pd.read_csv(path2)
# %%
"""# próba z cross-validation
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.model_selection import cross_val_score
model1 = RandomForestRegressor()
mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
scores = cross_val_score(model1, X, y, cv=5, scoring=mae_scorer)
print(scores)
print("Średni MAE:", -scores.mean())
print("Odchylenie standardowe:", scores.std())"""
# %%
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, max_error
#  dzielimy na model treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=2137)
# w treakcie testowania dobrałem najlepsze parametry
forest = RandomForestRegressor(n_estimators=500,max_depth=20, n_jobs=-1,random_state=2137)
# dopasowujemy model
forest.fit(X_train, y_train)
# %% testujemy
y_pred = forest.predict(X_test)
mae_test = mean_absolute_error(y_test, y_pred)
rmse_test = root_mean_squared_error(y_test, y_pred)
r2_test = r2_score(y_test, y_pred)
max_test = max_error(y_test, y_pred)
print(f"MAE:  {mae_test:.2f}") # Mean Absolute Error
print(f"RMSE: {rmse_test:.2f}") # Root Mean Squared Error
print(f"R²:   {r2_test:.3f}") # współczynnik determinacji
print(f"max error:   {max_test:.3f}")
# %% inne merryki
from sklearn.metrics import mean_absolute_percentage_error,median_absolute_error
mape = mean_absolute_percentage_error(y_test, y_pred)
medae = median_absolute_error(y_test, y_pred)
print(f"MAPE: {mape*100:.2f}%")
print(f"MedianAE: {medae:.2f}")
# %%
y_test = np.array(y_test).reshape(347)
results = pd.DataFrame(dict(prediction = np.array(y_pred), real = y_test))
results.loc[:,"absolute_error"] = (results.loc[:,"prediction"]-results.loc[:,"real"]).abs()
results.loc[:,"relative_error[%]"] = results.loc[:,"absolute_error"]*100/results.loc[:,"real"]
len(results.loc[results.loc[:,"relative_error[%]"]>10,:])/len(results) # <12%
results.sort_values(by = "relative_error[%]")
# %% Wykres przewidywania vs rzeczywistość
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Rzeczywiste kalorie")
plt.ylabel("Przewidywane kalorie")
plt.title("Predykcja vs Rzeczywistość")
plt.grid(True)
plt.show()
# %%
errors = y_test - y_pred
plt.figure(figsize=(8, 5))
plt.hist(errors, bins=40, edgecolor='black')
plt.title("Histogram błędów predykcji")
plt.xlabel("Błąd predykcji [kcal]")
plt.ylabel("Liczba przypadków")
plt.grid(True)
plt.tight_layout()
plt.show()
# %%
rel_errors = errors*100/y_test
plt.figure(figsize=(8, 5))
plt.hist(rel_errors, bins=40, edgecolor='black')
plt.title("Histogram względnych błędów predykcji")
plt.xlabel("Względny błąd predykcji [%]")
plt.ylabel("Liczba przypadków")
plt.grid(True)
plt.tight_layout()
plt.show()
# %%
forest.fit(X,y)
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
# %%
from sklearn.inspection import PartialDependenceDisplay
f_to_plot = ['total_movements', 'active_time[s]', 'training_effect']
fig, ax = plt.subplots(figsize=(12, 4))
PartialDependenceDisplay.from_estimator(forest, X_train, f_to_plot, ax=ax)
plt.suptitle("Partial Dependence Plots")
plt.tight_layout()
plt.show()
# %%
from sklearn.tree import plot_tree

tree = forest.estimators_[0] # pierwsze drzewo
plt.figure(figsize=(30, 15))
plot_tree(tree, feature_names=X.columns, filled=True, max_depth=3)
plt.title("Jedno z drzew w Random Forest")
plt.show()
# %%
import plotly.express as px
wyk = px.scatter(results,
                 x='real',
                 y='prediction',
                 trendline='ols',
                 title='predicted vs real calories')
wyk.update_traces(marker_size=5, marker_color='blue')
for trace in wyk.data: trace.line.color = 'red'
wyk.show()
# %%
import pickle
with open('model_rf.pkl', 'wb') as f:
    pickle.dump(forest, f)