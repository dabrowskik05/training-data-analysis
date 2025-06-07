# %%
import pandas as pd
import DataSimplifyingCsv as DaneCsv
import DataSimplifyingJson as DaneJson

# %%
df_csv = DaneCsv.df
df_json = DaneJson.df
# %%
# Literally everything (with duplicates)
merged_df = pd.merge(df_json, df_csv, on='session_id', how='left')
    
# %%

merged_df.to_csv('zmergowane_dane.csv', index=False)
# %%

# Most important data
summarised_df = merged_df.loc[:, merged_df.columns.tolist()[0:10] + 
                          ['total_strokes', 'calories', 'total_ascent', 'total_descent', 'training_effect', 'anaerobic_effect', 'total_strides' ]
                           + df_csv.columns.tolist()[2:len(df_csv.columns)] + ['session_id'] ]
# %%
rename_dict = {
    "start_date": "Start_Date",
    "end_date": "End_Date",
    "start_day": "Start_Day",
    "end_day": "End_Day",
    "start_time": "Start_Time",
    "end_time": "End_Time",
    "start_latitude": "Start_Latitude",
    "start_longitude": "Start_Longitude",
    "elapsed_time": "Elapsed_Time",
    "active_time": "Active_Time",
    "total_strokes": "Total_Strokes",
    "calories": "Calories",
    "total_ascent": "Total_Ascent",
    "total_descent": "Total_Descent",
    "training_effect": "Training_Effect",
    "anaerobic_effect": "Anaerobic_Effect",
    "total_strides": "Total_Strides",
}

summarised_df = summarised_df.rename(columns=rename_dict)

# %%
