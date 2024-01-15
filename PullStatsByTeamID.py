import os
import requests
import json
import csv
import pandas as pd

# Define output CSV filename
file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/TeamIDs.csv' 

# Read the CSV file into a DataFrame
teamsdf = pd.read_csv(file_path)
teams = teamsdf.iloc[:, 1].tolist()
print(teams)
for team in teams:
    team1 = str(team)
    team1_csv = 'team' + team1 +'.csv'
    # Set up the API URL with your team ID
    url = f"https://proclubs.ea.com/api/nhl/clubs/matches?clubIds={team1}&platform=common-gen5&matchType=club_private"

    # Set up headers to mimic a browser request
    headers = {
        'Referer': 'www.ea.com',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Connection': 'keep-alive'
    }

    # Make a GET request to the API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Specify the directory path and filename for json
        directory = 'C:/Users/Noah/Desktop/Code/NHL_clean/Output_Excel/Stats'  # Modify this with your desired directory
        ''' - Dont need to save json unless error testing
        filename = 'raw_data.json'  # Modify this with your desired filename

        # Save the JSON data to a file in the specified directory
        with open(f'{directory}/{filename}', 'w') as file:
            json.dump(data, file)  # Save the JSON data to a file in the specified directory
        '''

        # Process JSON data and write to CSV file
        output_file = os.path.join('C:/Users/Noah/Desktop/Code/NHL_clean/Stats', team1_csv)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            first_iteration=True
            header = ['matchID', 'timestamp']
            # Iterate through JSON data and write rows to CSV
            for item in data:
                match_id = item['matchId']
                timestamp = item['timestamp']
                
                # Access the "players" section within each item
                players_info = item.get('players', {})
                # Iterate through the player information
                for club_id, player in players_info.items():
                    # Process player data here
                    # For example, print player IDs and their data
                    #print("Club ID:", club_id)
                    #print("Player ID:", player)
                    for player_ID, player_stats in player.items():
                        row=[match_id, timestamp]
                        #print("Player_ID:", player_ID)
                        #print("Stats:", player_stats)
                        for stat in player_stats.items():
                            #print("Stat:", stat)
                            #print(stat[1])
                            header= header + [stat[0]]
                            row = row + [stat[1]]
                        if first_iteration:
                            csv_writer.writerow(header)
                            first_iteration=False
                        csv_writer.writerow(row)        

        print(f'Data retrieved and stored as {output_file}')
    else:
        print('Failed to retrieve data.')
