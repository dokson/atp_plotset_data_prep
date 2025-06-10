import pandas as pd

rankings_2024 = pd.read_csv('../atp_rankings_24.csv')
rankings_2024 = rankings_2024[rankings_2024['rank'].between(1, 10)].drop_duplicates()

rankings_2025 = pd.read_csv('../atp_rankings_25.csv')

all_rankings = pd.concat([rankings_2024, rankings_2025], ignore_index=True)

players = pd.read_csv('../atp_players.csv')
players['player_name'] = players['name_first'] + ' ' + players['name_last']

ranking_data = all_rankings.merge(players, left_on='player', right_on='player_id')
ranking_data['ranking_date'] = pd.to_datetime(ranking_data['ranking_date'], format="%Y%m%d").dt.strftime('%d/%m/%Y')

pivot_data = ranking_data.pivot_table(index='player_name', columns='ranking_date', values='points').astype('Int64')

# Add image URLs for players
players_images = pd.read_csv('../players_images.csv')
pivot_data = pivot_data.merge(players_images, on='player_name', how='left')

# Reordering columns to have player_image_url at the beginning after player_name
dates = [col for col in pivot_data.columns if col not in ['player_name', 'player_image_url']]
dashboard_data = pivot_data[['player_name', 'player_image_url'] + dates]

# Check for players without images
missing_players = dashboard_data[dashboard_data['player_image_url'].isna()]['player_name'].tolist()
if missing_players:
    print("There are players without an image", missing_players)
# Save dashboard data to CSV file
else:
    print(dashboard_data)
    dashboard_data.to_csv("dashboard.csv" , index=False)
