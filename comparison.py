# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# %%
path1 = "zebrane_dane_y.csv"
path2 = "zebrane_dane_X.csv"
X = pd.read_csv(path2)
y = pd.read_csv(path1)
# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2137)
forest = RandomForestRegressor(n_estimators=500,max_depth=20, random_state=2137, n_jobs=-1)
forest.fit(X_train, y_train)
y_pred_rf = forest.predict(X_test)
linreg = LinearRegression()
linreg.fit(X_train, y_train)
y_pred_lr = linreg.predict(X_test)
# %%
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score,max_error,mean_absolute_percentage_error,median_absolute_error
def metrics(x):
    return{"MAE":mean_absolute_error(y_test,x),"RMSE":root_mean_squared_error(y_test,x),
    "Max_error": max_error(y_test,x),"R2":r2_score(y_test,x), 
    "mape":mean_absolute_percentage_error(y_test,x)*100,"medae":median_absolute_error(y_test,x)}

df_results = pd.DataFrame({"Linear Regression": metrics(y_pred_lr),
                           "Random Forest": metrics(y_pred_rf)})
round(df_results,2)
# %%
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred_lr, alpha=0.5, label='Linear Regression')
plt.scatter(y_test, y_pred_rf, alpha=0.5, label='Random Forest')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ideal')
plt.xlabel("Rzeczywiste kalorie")
plt.ylabel("Przewidywane kalorie")
plt.title("Predykcja vs Rzeczywistość")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
# %%
forest.fit(X,y)
linreg.fit(X,y)
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
# LR jest łatwy do interpretacji — mamy wzór,
#🌲 RF jest trochę „czarną skrzynką”, ale bardziej dokładny.
# RF może lepiej radzić sobie z nieliniowościami i interakcjami cech.
# #LR zakłada liniowe zależności i jest podatny na outliery.
# %%
from sklearn.model_selection import cross_val_score

cv_lr = cross_val_score(forest, X, y, cv=5, scoring='r2')
cv_rf = cross_val_score(linreg, X, y, cv=5, scoring='r2')

print("CV R2 Linear Regression:", cv_lr.mean())
print("CV R2 Random Forest:", cv_rf.mean())
# można też:'max_error','neg_mean_absolute_error','neg_mean_squared_error','neg_root_mean_squared_log_error', 
# 'neg_mean_absolute_percentage_error','neg_median_absolute_error','neg_root_mean_squared_error'