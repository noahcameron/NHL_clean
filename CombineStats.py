import pandas as pd
import glob
import os

# Replace 'path/to/folder' with the actual folder path containing your CSV files
folder_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/Stats/*.csv'  # Adjust the extension if your files have a different extension

# Step 1: Get a list of file paths for all CSV files in the folder
csv_files = glob.glob(folder_path)

# Step 2: Read each CSV file and store them as DataFrames in a list
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Step 3: Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)
# Also concat existing data
file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/StatsCombined/CombinedStats.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Remove duplicates based on the composite key
combined_df = combined_df.drop_duplicates(subset=['matchID', 'playername'])

#Filter by after 8:30
# Read the CSV file containing the game IDs you want to filter by
# Replace 'new_file_path' with the path to your new CSV file containing game IDs
new_file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/GameIDs/LGCodes.csv'  # Replace this with the path to your new CSV file
GameIDs = pd.read_csv(new_file_path)
# Convert epoch time to datetime format
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], unit='s')
# Localize to a specific timezone (e.g., 'America/New_York')
combined_df['timestamp'] = combined_df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')
# Filter for times later than 20:30
combined_df = combined_df[combined_df['timestamp'].dt.time > pd.to_datetime('20:30').time()]

# Make sure game is against a valid LG opponent
new_file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/TeamIDs.csv'  
LGTeamIDs_df = pd.read_csv(new_file_path)
# Merge DataFrames based on the opponent/team ID columns with different names
combined_df = pd.merge(combined_df, LGTeamIDs_df, left_on='opponentClubId', right_on='TeamID', how='inner')

# Make sure data is for all 12 players in game
gameID_counts = combined_df['matchID'].value_counts()
# Get gameIDs that have exactly 10 entries
valid_gameIDs = gameID_counts[gameID_counts >= 10].index
# Filter the DataFrame to keep only rows with valid gameIDs
combined_df = combined_df[combined_df['matchID'].isin(valid_gameIDs)]

# Write to combined Stats
print(combined_df)
file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/StatsCombined/CombinedStats.csv'  # Replace this with your desired file path
combined_df.to_csv(file_path, index=False)  # Set index=False to avoid writing row numbers as the first column

print(f"DataFrame has been successfully written to '{file_path}'")