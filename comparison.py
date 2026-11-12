# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# %%
path1 = "zebrane_dane_Y.csv"
path2 = "zebrane_dane_X.csv"
X = pd.read_csv(path2)
Y = pd.read_csv(path1)
# %%
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2137)
forest = RandomForestRegressor(n_estimators=500,max_depth=20, random_state=2137, n_jobs=-1)
forest.fit(X_train, Y_train)
Y_pred_rf = forest.predict(X_test)
linreg = LinearRegression()
linreg.fit(X_train, Y_train)
Y_pred_lr = linreg.predict(X_test)
# %%
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score,max_error,mean_absolute_percentage_error,median_absolute_error
def metrics(x):
    return{"Mean absolute error":mean_absolute_error(Y_test,x),"Root mean squared error":root_mean_squared_error(Y_test,x),
    "Max error": max_error(Y_test,x),"R2":r2_score(Y_test,x), 
    "Mean absolute percentage erre":mean_absolute_percentage_error(Y_test,x)*100,"Median absolute error":median_absolute_error(Y_test,x)}

df_results = pd.DataFrame({"Linear Regression": metrics(Y_pred_lr),
                           "Random Forest": metrics(Y_pred_rf)})
round(df_results,3)
# %%
plt.figure(figsize=(6, 6))
plt.scatter(Y_test, Y_pred_lr, alpha=0.5, label='Linear Regression')
plt.scatter(Y_test, Y_pred_rf, alpha=0.5, label='Random Forest')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--', label='Ideal')
plt.xlabel("Rzeczywiste kalorie")
plt.ylabel("Przewidywane kalorie")
plt.title("Predykcja vs Rzeczywistość")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
# %%
forest.fit(X,Y)
linreg.fit(X,Y)
# %%
lr_importance = (pd.Series(linreg.coef_[0], index=X.columns)*X.std()).abs()
lr_importance = lr_importance/sum(lr_importance)
rf_importance = pd.Series(forest.feature_importances_, index=X.columns)

fig, ax = plt.subplots(1, 2, figsize=(14, 6))
lr_importance.sort_values().plot(kind='barh', ax=ax[0], title='Linear Regression')
rf_importance.sort_values().plot(kind='barh', ax=ax[1], title='Random Forest')
plt.tight_layout()
plt.show()
# %%