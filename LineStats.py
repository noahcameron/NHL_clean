# Line stats!

import pandas as pd
from itertools import combinations

#USER INPUT
minGP = 4
outputCSV = 'C:/Users/Noah/Desktop/Code/NHL_clean/StatsCombined/LineStats.csv'

# Assuming 'df' is your DataFrame containing player stats and 'player_name' is the column with player names
# Replace 'df' and 'player_name' with your actual DataFrame and column name

# Read in combined stats
file_path = 'C:/Users/Noah/Desktop/Code/NHL_clean/StatsCombined/CombinedStats.csv'
df = pd.read_csv(file_path)

# Group by 'matchID' and aggregate player names for each match
grouped_matches = df.groupby('matchID')['playername'].agg(list).reset_index()
#print(grouped_matches)

# Create a dictionary to store match IDs where player combinations appear together
player_combinations = {}

# Iterate through each match's player list to track match IDs for combinations
# definition of dict: (combination, [gp, [list of gameIDs]]
for index, row in grouped_matches.iterrows():
    for combo in combinations(row['playername'], 3):  # Change '3' to the size of player combinations you want
        combo_key = tuple(sorted(combo))
        if combo_key in player_combinations:
            player_combinations[combo_key] = (player_combinations[combo_key][0] + 1, player_combinations[combo_key][1] + [row['matchID']])
        else:
            player_combinations[combo_key] = (1, [row['matchID']])
#print(player_combinations)

# Filter combinations that appeared in at least three different matches
player_combinations_minGP = {k: v for k, v in player_combinations.items() if v[0]>=minGP}
#print(result)

# Dictionary to store player combinations and their corresponding scores
player_scores = {}

# Iterate through the player_combinations dictionary
for players, data in player_combinations_minGP.items():
    first_player = players[0]  # Extract the first player's name
    
    _, match_ids = data  # Extract match IDs for the current player combination
    
    # Filter the original DataFrame based on the first player's name and match IDs for the current combination
    filtered_stats = df[(df['playername'] == first_player) & (df['matchID'].isin(match_ids))]
    
    # Extract 'score' and 'opponentScore' for these match IDs and store them in the dictionary
    scores = filtered_stats.groupby('matchID')['score', 'opponentScore'].apply(lambda x: x.values.tolist()).to_dict()
    
    # Assign scores to the corresponding player combination in the dictionary
    player_scores[players] = scores

# Display the resulting dictionary with player combinations and their scores
#print(player_scores)

# Dictionary to store simplified scores and record for each player combination
simplified_scores = {}

# Iterate through the player_scores dictionary
for players, scores in player_scores.items():
    # Initialize sums for 'opponentScore' and 'score'
    opponent_score_sum = 0
    score_sum = 0
    wins = 0
    losses = 0
    
    # Iterate through match IDs and calculate sums and record
    for match_id, match_scores in scores.items():
        opponent_score_sum += sum([score[0] for score in match_scores])
        score_sum += sum([score[1] for score in match_scores])
        
        # Check for wins/losses based on scores comparison
        for score_pair in match_scores:
            if score_pair[0] > score_pair[1]:
                wins += 1
            else:
                losses += 1
    
    # Assign sums and record to the corresponding player combination in the simplified dictionary
    simplified_scores[players] = [opponent_score_sum, score_sum, wins, losses]

# Display the resulting dictionary with simplified scores and record
#print(simplified_scores)

# Dictionary to store simplified scores, record, win%, goal difference, and GP for each player combination
final_stats = {}

# Iterate through the player_scores dictionary
for players, scores in player_scores.items():
    # Initialize variables
    score_sum = 0
    opponent_score_sum = 0
    wins = 0
    losses = 0
    goals_for = 0
    goals_against = 0
    gp = 0
    
    # Iterate through match IDs and calculate sums, record, and goals
    for match_id, match_scores in scores.items():
        score_sum += sum([score[0] for score in match_scores])
        opponent_score_sum += sum([score[1] for score in match_scores])
        
        # Count wins/losses and calculate goals for and against
        for score_pair in match_scores:
            if score_pair[0] > score_pair[1]:
                wins += 1
                goals_for += score_pair[0]
                goals_against += score_pair[1]
            else:
                losses += 1
                goals_for += score_pair[0]
                goals_against += score_pair[1]
        
        gp += len(match_scores)  # Increment games played by the number of matches
    
    # Calculate win percentage, goal difference, and finalize GP
    win_percentage = (wins / (wins + losses)) * 100 if (wins + losses) != 0 else 0
    goal_difference = goals_for - goals_against
    
    # Assign values to the corresponding player combination in the final stats dictionary
    final_stats[players] = [
        score_sum,
        opponent_score_sum,
        wins,
        losses,
        win_percentage,
        goal_difference,
        gp
    ]

# Display the resulting dictionary with all statistics
#print(final_stats)

# Convert the dictionary to a DataFrame
stats_df = pd.DataFrame.from_dict(final_stats, orient='index', columns=[
    'GF',
    'GA',
    'Wins',
    'Losses',
    'Win_Percentage',
    'Goal_Difference',
    'Games_Played'
])

# Write the DataFrame to a CSV file
stats_df.to_csv(outputCSV)