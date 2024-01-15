import requests
from bs4 import BeautifulSoup
import csv
import os

# Set up headers to mimic a browser request
headers = {
    'Referer': 'www.ea.com',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Connection': 'keep-alive'
}

base_url = 'https://www.leaguegaming.com/forums/index.php?leaguegaming/league&action=league&page=game&gameid='
# USER INPUT --------------------------------------------------------------------------
firstGameID = 776390
gamesToCheck = 3 #Use 150 on lg night (30*3 + overshoot and lag outs)
output_sheet = 'LGCodes_Day1.csv'
# --------
output_file = os.path.join('C:/Users/Noah/Desktop/Code/NHL_clean/GameIDs', output_sheet)
# -------------------------------------------------------------------------------------
numbers = list(range(firstGameID, firstGameID + gamesToCheck)) + [7799999]
game_ids = numbers

LG_GameIDs = []

for game_id in game_ids:
    url = f"{base_url}{game_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        html_content = response.text  # Using .text to get text content

        soup = BeautifulSoup(html_content, 'html.parser')
        game_deleted = soup.find(text="This game no longer exists or was deleted.")
        if game_deleted:
            #print(f"Game with ID {game_id} no longer exists or was deleted.")
            None
        else:
            #print(f"Game with ID {game_id} exists.")
            LG_GameIDs = LG_GameIDs + [game_id]

        '''
        file_name = f"game_{game_id}.html"
        file_path = f"C:/Users/Noah/Desktop/Code/NHL/Output_Excel/{file_name}"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
            print(f"HTML content for Game ID {game_id} written to {file_path}")
        '''
    else:
        print(f"Failed to fetch data for game ID {game_id}")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['gameID'])  
        for gameID in LG_GameIDs:
            csv_writer.writerow([gameID])  

#this will overwrite current codes
output_sheet = 'LGCodes.csv'
output_file = os.path.join('C:/Users/Noah/Desktop/Code/NHL_clean/GameIDs', output_sheet)
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['gameID'])  
        for gameID in LG_GameIDs:
            csv_writer.writerow([gameID])  
print(LG_GameIDs)