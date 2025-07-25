import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression

# Import of Garmin Data
df = pd.read_csv('garmin_activities.csv')  

# Filter to only Running activity type
df = df[df['Activity Type'] == 'Running']

#filters out Avg Pace values without a value
df = df[df['Avg Pace'].str.contains(":", na=False)]

# Cleanup of the data, removing points of low distances short activity times
df = df[df['Distance'] > 1]

# Converting strings to numbers
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
df['Avg HR'] = pd.to_numeric(df['Avg HR'], errors='coerce')
df['Avg Pace'] = df['Avg Pace'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)

# Function to change pace from decimal to 'min/mile/ in graphs
def format_pace(decimal_pace):
    if pd.isna(decimal_pace):
        return None
    minutes = int(decimal_pace)
    seconds = int(round((decimal_pace - minutes) * 60))
    return f"{minutes}:{seconds:02}"

df['Avg Pace str'] = df['Avg Pace'].apply(format_pace)

# # Plot 1: Pace/Time
# plt.figure(figsize=(10,4))
# sns.lineplot(x='Date', y='Avg Pace', data=df)
# plt.title("Avg Pace over Time (min/mi)")
# plt.ylabel("Pace (min/mi)")
# plt.xlabel("Date of Activity")
# plt.tight_layout()
# plt.savefig("plots/pace_over_time.png")
# plt.close()

# # Plot 2: Avg HR/Pace 
# plt.figure(figsize=(10, 4))
# sns.lineplot(x='Avg Pace', y='Avg HR', data=df)
# plt.title("Avg Heart Rate over Avg. Pace")
# plt.ylabel("Average Heart Rate (bpm)")
# plt.xlabel("Average Pace")
# plt.tight_layout()
# plt.savefig("plots/avgHR_over_time.png")
# plt.close()

# # Plot 3: Avg. HR vs. Avg. Pace
# plt.figure(figsize=(8, 5))
# sns.scatterplot(x='Avg Pace', y='Avg HR', data=df)
# plt.title('Heart Rate vs Pace')
# plt.xlabel('Pace (min/mi)')
# plt.ylabel('Average Heart Rate (bpm)')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("plots/hr_vs_pace.png")
# plt.show()

# sns.lmplot(x='Avg Pace', y='Avg HR', data=df)
# plt.title('Heart Rate vs Pace with Trend Line')
# plt.xlabel('Pace (min/km)')
# plt.ylabel('Average Heart Rate (bpm)')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("plots/hr_vs_pace_trend.png")

# print("✅ Analysis complete. Plots saved in /plots folder.")

# lmplot returns a FacetGrid object
g = sns.lmplot(x='Avg Pace', y='Avg HR', data=df)

# Invert x-axis if lower pace = faster
g.ax.invert_xaxis()

# Format x-ticks as mm:ss
def format_pace(p):
    minutes = int(p)
    seconds = int(round((p - minutes) * 60))
    return f"{minutes}:{seconds:02}"

# Apply custom tick labels
ticks = g.ax.get_xticks()
labels = [format_pace(t) for t in ticks]
g.ax.set_xticklabels(labels)

# Set axis titles
g.set_axis_labels("Pace (min/mile)", "Heart Rate (bpm)")

plt.tight_layout()
plt.show()

#-----------------------------
# Training a simple LR model using multiple datapoints
model = LinearRegression()
X = df[['Avg HR', 'Distance']] 
y = df['Avg Pace']
model.fit(X, y)

# Predict and print result
prediction = model.predict([[150, 31.0]])  # Example input
print(f"Predicted race time: {prediction[0]:.2f} minutes")
