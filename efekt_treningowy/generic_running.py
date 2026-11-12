# %%

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau
import statsmodels.api as sm
from scipy import stats

# Wczytanie danych
df = pd.read_csv('generic_running.csv')

# Wybór kolumn
num_cols = [
    'distance [km]', 'active_time [s]', 'total_ascent [m]', 
    'avg_hr [bpm]', 'max_hr [bpm]',
    'calories [kcal]',
    'avg_temperature [°C]'
]
target = 'training_effect'


# %%
# Krok 2: Analiza korelacji
corr_matrix = pd.DataFrame(index=num_cols, columns=['spearman', 'kendall', 'p_value'])

for col in num_cols:
    # Korelacja Spearmana
    spear_corr, spear_p = spearmanr(df[col], df[target], nan_policy='omit')
    
    # Korelacja Kendalla
    kendall_corr, kendall_p = kendalltau(df[col], df[target], nan_policy='omit')
    
    corr_matrix.loc[col] = [spear_corr, kendall_corr, spear_p]

# Filtracja istotnych statystycznie
significant_corr = corr_matrix[corr_matrix['p_value'].astype(float) < 0.05]
significant_corr = significant_corr.sort_values('spearman', key=abs, ascending=False)

print("\nNajsilniejsze korelacje z training_effect:")
print(significant_corr[['spearman', 'kendall']])
# %%
# Krok 3: Analiza grupowa - intensywność
intensity_bins = [0, 115, 134, 154, 174, 193]
intensity_labels = ['Bardzo lekki', 'Lekki', 'Umiarkowany', 'Intensywny', 'Maksymalny']

df['intensity_group'] = pd.cut(
    df['avg_hr [bpm]'],
    bins=intensity_bins,
    labels=intensity_labels
)

intensity_stats = df.groupby('intensity_group')[target].agg(['mean', 'std', 'count'])
print("\nEfekt treningowy w grupach intensywności:")
print(intensity_stats)

# Krok 4: Analiza czasowa
df['duration_group'] = pd.cut(
    df['active_time [s]'] / 60,  # w minutach
    bins=[0, 30, 60, 90, 120, 1000],
    labels=['<30min', '30-60min', '60-90min', '90-120min', '>120min']
)

duration_stats = df.groupby('duration_group')[target].agg(['mean', 'std'])
print("\nEfekt treningowy w grupach czasowych:")
print(duration_stats)

# Krok 5: Wizualizacje
plt.figure(figsize=(15, 10))

# Wykres 1: Efekt vs intensywność
plt.subplot(2, 2, 1)
sns.boxplot(
    x='intensity_group',
    y=target,
    data=df,
    showfliers=False,
    palette='viridis'
)
plt.title('Efekt treningowy wg intensywności')
plt.xlabel('Grupa intensywności')
plt.grid(axis='y')

# Wykres 2: Efekt vs czas trwania
plt.subplot(2, 2, 2)
sns.boxplot(
    x='duration_group',
    y=target,
    data=df,
    showfliers=False,
    palette='rocket'
)
plt.title('Efekt treningowy wg czasu trwania')
plt.xlabel('Czas trwania')
plt.grid(axis='y')

# Wykres 3: Zależność od najsilniejszej cechy
if not significant_corr.empty:
    top_feature = significant_corr.index[0]
    plt.subplot(2, 2, 3)
    sns.scatterplot(
        x=top_feature,
        y=target,
        data=df,
        alpha=0.6,
        color='purple'
    )
    plt.title(f'Zależność od {top_feature}')
    plt.grid(True)

# Wykres 4: Interakcja intensywność-czas
plt.subplot(2, 2, 4)
interaction_data = df.pivot_table(
    values=target,
    index='intensity_group',
    columns='duration_group',
    aggfunc='mean'
)
sns.heatmap(
    interaction_data,
    annot=True,
    fmt=".2f",
    cmap='coolwarm'
)
plt.title('Interakcja: intensywność-czas')
plt.xlabel('Czas trwania')
plt.ylabel('Intensywność')

plt.tight_layout()
plt.savefig('generic_running_training_effect_analysis.png', dpi=300)
plt.show()