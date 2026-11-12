# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
path1 = "zebrane_dane_Y.csv"
path2 = "zebrane_dane_X.csv"
X = pd.read_csv(path2)
Y = pd.read_csv(path1)
# %%
X
# %%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, max_error
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=2137)
linreg = LinearRegression()
linreg.fit(X_train, Y_train)
Y_pred = linreg.predict(X_test)
# %%
print("MAE: ",mean_absolute_error(Y_test, Y_pred))
print("RMSE: ", root_mean_squared_error(Y_test, Y_pred))
print("R²: ",r2_score(Y_test, Y_pred))
print("Max error:", max_error(Y_test, Y_pred))
# %%
from sklearn.metrics import mean_absolute_percentage_error,median_absolute_error
mape = mean_absolute_percentage_error(Y_test, Y_pred)
medae = median_absolute_error(Y_test, Y_pred)
print(f"MAPE: {mape*100}%")
print(f"MedianAE: {medae}")
# %%
Y_pred = Y_pred.reshape(284)
Y_test = np.array(Y_test).reshape(284)
results = pd.DataFrame(dict(prediction = np.array(Y_pred), real = Y_test))
results.loc[:,"absolute_error"] = (results.loc[:,"prediction"]-results.loc[:,"real"]).abs()
results.loc[:,"relative_error[%]"] = results.loc[:,"absolute_error"]*100/results.loc[:,"real"]
len(results.loc[results.loc[:,"relative_error[%]"]>10,:])/len(results) # <30%
results.sort_values(by = "relative_error[%]")
# jeden 98.5% błędu, reszta <60%
# %%
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
plt.title("Histogram błędów bezwzględnych")
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
plt.xlabel("Względny błąd predykcji [%]")
plt.ylabel("Liczba przypadków")
plt.grid(True)
plt.tight_layout()
plt.show()
# %%
linreg.fit(X,Y)
# %%
coeffs = pd.Series(linreg.coef_[0], index=X.columns)
print(coeffs.sort_values(key=abs, ascending=False))
# %%
plt.figure(figsize=(10, 8))
coeffs.sort_values(key=abs).plot(kind='barh', color='skyblue')
plt.title('Wartość współczynników dla poszczególnych cech w regresji liniowej')
plt.xlabel('Współczynnik regresji')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()
# %%
# przeskalujemy
X = X.astype("float64")
importances = (coeffs*X.std()).abs()
importances = importances/sum(importances)
plt.figure(figsize=(10, 8))
importances.sort_values().plot(kind='barh', color='skyblue')
plt.title('Wagi cech w regresji liniowej')
plt.xlabel('Waga cechy')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()
X.std()
# %%
from sklearn.inspection import PartialDependenceDisplay
fig, ax = plt.subplots(figsize=(12, 8))
PartialDependenceDisplay.from_estimator(linreg, X_train, 
    ['active_time[s]','lap_count',"training_effect",'avg_hr[bpm]',"sport_running","max_hr[bpm]"], ax=ax)
plt.suptitle("Wykresy zależności cząstkowych dla regresji liniowej")
plt.tight_layout()
plt.show()
# %%
intercept = linreg.intercept_ # wyraz wolny
print("Równanie regresji liniowej:")
for feature, coef in coeffs.sort_values(key=abs,ascending = False).items():
    print(f"{coef:+.3f} * {feature}")
print(f"{intercept[0]:+.3f}")