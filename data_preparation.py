import pandas as pd
import os
from datetime import datetime

# Parameters
starting_date = 20230101
top_n = 10

# If deeper history is needed, read all rankings files
if starting_date < 20200101:
    rankings_files = [f for f in os.listdir('data/') if f.startswith('atp_rankings_') and f.endswith('s.csv')]
    rankings_history = pd.DataFrame()

    # Load and process rankings history files
    for file in rankings_files:
        file_path = os.path.join('data/', file)
        df = pd.read_csv(file_path)
        rankings_history = pd.concat([rankings_history, df], ignore_index=True)
else:
    rankings_history = pd.read_csv('data/atp_rankings_20s.csv')

# Cast columns to integer for filtering
rankings_history['ranking_date'] = pd.to_numeric(rankings_history['ranking_date']).astype('Int64')
rankings_history['rank'] = pd.to_numeric(rankings_history['rank']).astype('Int64')
# Filter rankings history for top N players and starting date
rankings_history = rankings_history[
    (rankings_history['rank'].between(1, top_n)) & 
    (rankings_history['ranking_date'] >= starting_date)].drop_duplicates()

rankings_current = pd.read_csv('data/atp_rankings_current.csv')

all_rankings = pd.concat([rankings_history, rankings_current], ignore_index=True)

# Load players data to get full names
players = pd.read_csv('data/atp_players.csv', low_memory=False)
players['player_name'] = players['name_first'] + ' ' + players['name_last']

ranking_data = all_rankings.merge(players, left_on='player', right_on='player_id')
ranking_data['ranking_date'] = pd.to_datetime(ranking_data['ranking_date'], format="%Y%m%d").dt.strftime('%d/%m/%Y')

# Create pivot table
pivot_data = ranking_data.pivot_table(index='player_name', columns='ranking_date', values='points').astype('Int64')

# Add image URLs for players
players_images = pd.read_csv('data/players_images.csv')
pivot_data = pivot_data.merge(players_images, on='player_name', how='left')

# Reordering columns to have player_image_url at the beginning after player_name
dates = [col for col in pivot_data.columns if col not in ['player_name', 'player_image_url']]
sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
dashboard_data = pivot_data[['player_name', 'player_image_url'] + sorted_dates]

# Check for players without images
missing_players = dashboard_data[dashboard_data['player_image_url'].isna()]['player_name'].tolist()
if missing_players:
    print("There are players without an image", missing_players)
# Save dashboard data to CSV file
else:
    print(dashboard_data)
    dashboard_data.to_csv("dashboard.csv" , index=False)
