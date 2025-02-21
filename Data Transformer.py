import pandas as pd

# Load the Excel file
file_path = 'syntheticdata_2yconsistent.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Filter the columns containing 'demand' (adjust if necessary)
demand_columns = [col for col in df.columns if 'Demand (D) (Day)' in col]

# Use pd.melt() to reshape the DataFrame
df_melted = df.melt(id_vars=['Project ID'], 
                    value_vars=demand_columns,
                    var_name='Date', 
                    value_name='Demand')

# Extract Month and Year from the 'Date' column (e.g., "Jan 2023" from "Jan 2023 demand")
df_melted['Date'] = df_melted['Date'].str.extract(r'([A-Za-z]+ \d{4})')

# Convert the 'Date' column to datetime (will be sorted chronologically)
df_melted['Date'] = pd.to_datetime(df_melted['Date'])

# Group by 'Project ID' and 'Date', then aggregate demand (e.g., sum)
df_grouped = df_melted.groupby(['Project ID', 'Date'], as_index=False)['Demand'].sum()

# Now format the 'Date' column back to 'Month Year' (no time included)


# Sort the data by 'Project ID' and 'Date' in ascending order
df_grouped = df_grouped.sort_values(by=['Project ID', 'Date'])
df_grouped['Date'] = df_grouped['Date'].dt.strftime('%b %Y')

# Display the result
print(df_grouped)

# Optionally, save the reshaped and sorted data back to an Excel file
df_grouped.to_excel('syntheticdata_sorted2yearconsisten.xlsx', index=False)
