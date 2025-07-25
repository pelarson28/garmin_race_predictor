import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression

# Import of Garmin Data
df = pd.read_csv('garmin_activities.csv')  

# Filter to only Running activity type
df = df[df['Activity Type'] == 'Running']

# # Cleanup of the data, removing points of low distances short activity times
# df = df[df['Distance'] > 1]

#filters out Avg and Best Pace values without a value
df = df[df['Avg Pace'].str.contains(":", na=False)]
df = df[df['Best Pace'].str.contains(":", na=False)]
df = df[df['Avg GAP'].str.contains(":", na=False)]

# Converting strings to numbers
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
df['Avg HR'] = pd.to_numeric(df['Avg HR'], errors='coerce')
df['Avg Cadence'] = pd.to_numeric(df['Avg Cadence'], errors='coerce')
df['Avg Power'] = pd.to_numeric(df['Avg Power'], errors='coerce')
df['Avg Stride Length'] = pd.to_numeric(df['Avg Stride Length'], errors='coerce')
df['Best Pace'] = df['Best Pace'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)
df['Avg GAP'] = df['Avg GAP'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)
df['Avg Pace'] = df['Avg Pace'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)

# Create Speed column to inversely correlate Avg Pace for clarity
df['Avg Speed (mph)'] = 60 / df['Avg Pace']

# Heatmap column selection
cols_to_use = ['Avg HR','Avg Speed (mph)', 'Avg Cadence', 'Distance', 'Avg Power', 'Avg Stride Length']

# # Cleaning dataframe
# df_subset = df[cols_to_use].dropna()

# Entering the matrix
corr_matrix = df[cols_to_use].corr()

# Plotting heatmap
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix, annot=True, cmap="magma", fmt=".2f", center=0)
plt.title('Correlation Heatmap')
plt.savefig('garmin_heatmap.png', dpi=300, bbox_inches='tight')
