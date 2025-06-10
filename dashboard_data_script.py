import pandas as pd
from datetime import datetime

rankings_20s = pd.read_csv('data/atp_rankings_20s.csv')
rankings_20s['ranking_date'] = pd.to_numeric(rankings_20s['ranking_date']).astype('Int64')
rankings_20s['rank'] = pd.to_numeric(rankings_20s['rank']).astype('Int64')

rankings_23_24 = rankings_20s[
    (rankings_20s['rank'].between(1, 10)) & 
    (rankings_20s['ranking_date'] >= 20230101)].drop_duplicates()

rankings_2025 = pd.read_csv('data/atp_rankings_current.csv')

all_rankings = pd.concat([rankings_23_24, rankings_2025], ignore_index=True)

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
