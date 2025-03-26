import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


# Load the dataset
df = pd.read_csv('fifa21_raw_data.csv')

# Convert height to numerical form (in cm)
def convert_height(height):
    if isinstance(height, str):
        feet, inches = height.replace("'", " ").replace('"', '').split()
        return int(feet) * 30.48 + int(inches) * 2.54
    return np.nan

df['Height'] = df['Height'].apply(convert_height)

# Convert weight to numerical form (in kg)
def convert_weight(weight):
    if isinstance(weight, str):
        return float(weight.replace('lbs', '')) * 0.453592
    return np.nan

df['Weight'] = df['Weight'].apply(convert_weight)

# Remove unnecessary newline characters from all columns
df = df.replace('\n', '', regex=True)

# Check which players have been playing at a club for more than 10 years
df['Joined'] = pd.to_datetime(df['Joined'], errors='coerce')
df['Years_at_Club'] = (pd.to_datetime('2021-01-01') - df['Joined']).dt.days / 365
players_over_10_years = df[df['Years_at_Club'] > 10]

# Convert 'Value', 'Wage', and 'Release Clause' to numerical values
def convert_currency(value):
    if isinstance(value, str):
        if 'M' in value:
            return float(value.replace('€', '').replace('M', '')) * 1_000_000
        elif 'K' in value:
            return float(value.replace('€', '').replace('K', '')) * 1_000
        else:
            return float(value.replace('€', ''))
    return np.nan

df['Value'] = df['Value'].apply(convert_currency)
df['Wage'] = df['Wage'].apply(convert_currency)
df['Release Clause'] = df['Release Clause'].apply(convert_currency)

# Strip star characters from columns and convert to numerical
star_columns = ['W/F', 'SM', 'IR']
for col in star_columns:
    df[col] = df[col].str.replace('★', '').astype(float)

# Identify highly valuable but underpaid players
df['Value_to_Wage_Ratio'] = df['Value'] / df['Wage']
underpaid_players = df.sort_values(by='Value_to_Wage_Ratio', ascending=False).head(10)

# Scatter plot between Wage and Value
plt.figure(figsize=(10, 6))
plt.scatter(df['Wage'], df['Value'], alpha=0.5)
plt.title('Scatter Plot of Wage vs Value')
plt.xlabel('Wage (€)')
plt.ylabel('Value (€)')
plt.grid(True)
plt.show()

# Display the results
print("Players who have been at a club for more than 10 years:")
print(players_over_10_years[['Name', 'Joined', 'Years_at_Club']])

print("\nHighly valuable but underpaid players:")
print(underpaid_players[['Name', 'Value', 'Wage', 'Value_to_Wage_Ratio']])

# Scatter plot between Weight and Height
plt.figure(figsize=(10, 6))
plt.scatter(df['Weight'], df['Height'], alpha=0.5)
plt.title('Scatter Plot of Weight vs Height')
plt.xlabel('Weight (kg)')
plt.ylabel('Height (cm)')
plt.grid(True)
plt.show()

# Display the updated columns with the changes
print("\nUpdated columns with changes:")
print(df[['Height', 'Weight', 'W/F', 'SM', 'IR']].head())