# %%
import pandas as pd
import numpy as np
import DataSimplifyingCsv as DaneCsv
import DataSimplifyingJson as DaneJson

# %%
df_csv = DaneCsv.df
df_json = DaneJson.df
# %%

merged_df = pd.merge(df_json, df_csv, left_on='session_id', right_on='session_id', how='left')
    
# %%
