# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %%
path1 = "zebrane_dane_y.csv"
path2 = "zebrane_dane_X.csv"
X = pd.read_csv(path2)
y = pd.read_csv(path1)
# %%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, max_error
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2137)
linreg = LinearRegression()
linreg.fit(X_train, y_train)
y_pred = linreg.predict(X_test)
# %%
mae_lin = mean_absolute_error(y_test, y_pred)
rmse_lin = root_mean_squared_error(y_test, y_pred)
r2_lin = r2_score(y_test, y_pred)

print(f"MAE:  {mae_lin:.2f}")
print(f"RMSE: {rmse_lin:.2f}")
print(f"R²:   {r2_lin:.3f}")
print("Max error:", max_error(y_test, y_pred))
# %%
from sklearn.metrics import mean_absolute_percentage_error,median_absolute_error
mape = mean_absolute_percentage_error(y_test, y_pred)
medae = median_absolute_error(y_test, y_pred)
print(f"MAPE: {mape*100:.2f}%")
print(f"MedianAE: {medae:.2f}")
# %%
y_pred = y_pred.reshape(347)
y_test = np.array(y_test).reshape(347)
results = pd.DataFrame(dict(prediction = np.array(y_pred), real = y_test))
results.loc[:,"absolute_error"] = (results.loc[:,"prediction"]-results.loc[:,"real"]).abs()
results.loc[:,"relative_error[%]"] = results.loc[:,"absolute_error"]*100/results.loc[:,"real"]
len(results.loc[results.loc[:,"relative_error[%]"]>10,:])/len(results) # >30%
results.sort_values(by = "relative_error[%]")
# %%
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
plt.hist(errors, bins=30, edgecolor='black')
plt.title("Histogram błędów (residuals) — Linear Regression")
plt.xlabel("Błąd [kcal]")
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
linreg.fit(X,y)
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
importances.sort_values(key=abs).plot(kind='barh', color='skyblue')
plt.title('Wagi cech w regresji liniowej')
plt.xlabel('Waga cechy')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()
X.std()
# %%
from sklearn.inspection import PartialDependenceDisplay
f_to_plot = ['active_time[s]','lap_count','avg_hr[bpm]',"training_effect","total_movements","anaerobic_effect"]
fig, ax = plt.subplots(figsize=(12, 8))
PartialDependenceDisplay.from_estimator(linreg, X_train, f_to_plot, ax=ax)
plt.suptitle("Partial Dependence Plots")
plt.tight_layout()
plt.show()
# %%
intercept = linreg.intercept_ # wyraz wolny
print("Równanie regresji liniowej:")
for feature, coef in coeffs.items():
    print(f"{coef:+.2f} * {feature}")
print(f"+ ({intercept[0]:.2f})")
# %%

# %%
import pickle

# Załóżmy, że masz wytrenowany model rf
with open('model_lr.pkl', 'wb') as f:
    pickle.dump(linreg, f)