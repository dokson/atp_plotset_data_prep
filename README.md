# ATP Rankings Data Preparation for PlotSet Animated Dashboard

## Overview

This project generates data for a PlotSet animated dashboard that visualizes ATP (Association of Tennis Professionals) player rankings from 2023 onwards. The script processes historical and current ranking data, filters top-10 players, and creates a structured dataset with player information, images, and points progression over time.

**Key Features:**
    - Processes ATP rankings data from 2023 (but you can eventually start from 1970) to 2025
    - Filters and tracks top-10 players only
    - Merges player information and profile images
    - Generates time-series data in pivot table format
    - Validates data completeness before output

## Project Structure

```plaintext
project/
├── data/
│   ├── atp_players.csv           # Player information database
│   ├── atp_rankings_00s.csv      # Historical rankings (2000-2009)
│   ├── atp_rankings_10s.csv      # Historical rankings (2010-2019)
│   ├── atp_rankings_20s.csv      # Historical rankings (2020-2024)
│   ├── atp_rankings_70s.csv      # Historical rankings (1970-1979)
│   ├── atp_rankings_80s.csv      # Historical rankings (1980-1989)
│   ├── atp_rankings_90s.csv      # Historical rankings (1990-1999)
│   ├── atp_rankings_current.csv  # Current rankings (2025+)
│   └── players_images.csv        # Player image URL mappings
├── dashboard.csv                 # Generated output file
├── data_preparation.py           # Main data preparation script
└── README.md                     # This documentation
```

## Prerequisites

### System Requirements

- **Python 3.7+**
- **Memory**: Minimum 1GB RAM

### Required Libraries

```bash
pip install pandas
```

**Dependencies:**

- `pandas` >= 1.3.0
- `datetime` (built-in Python module)

## Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dokson/atp_plotset_data_prep
   cd tennis_atp
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   # or simply: pip install pandas
   ```

3. **Run the script:**

   ```bash
   python data_preparation.py
   ```

## Data Files Description

### Input Files

| File | Description | Columns | Format |
|------|-------------|---------|--------|
| `atp_players.csv` | Player information database | `player_id`, `name_first`, `name_last`, `hand`, `dob`, `ioc`, `height`, `wikidata_id` | Standard CSV |
| `atp_rankings_20s.csv` | Historical ATP rankings 2020-2024 | `ranking_date`, `rank`, `player`, `points` | Standard CSV |
| `atp_rankings_current.csv` | Latest rankings (2025+) | `ranking_date`, `rank`, `player`, `points` | Standard CSV |
| `players_images.csv` | Player image URL mappings | `player_name`, `player_image_url` | Standard CSV |

### Output File

**`dashboard.csv`** - Final data for PlotSet having structure:
    - `player_name`: Full player name
    - `player_image_url`: Profile image URL
    - Date columns (DD/MM/YYYY): for each ranking_date

## Script Workflow

### Data Processing Pipeline

1. **📊 Data Loading & Filtering**
   - Load historical rankings from `atp_rankings_20s.csv`
   - Convert data types for proper processing
   - Filter for top-10 players (ranks 1-10) from 2023-01-01 onwards
   - Remove duplicate entries

2. **🔗 Data Integration**
   - Load current rankings from `atp_rankings_current.csv`
   - Concatenate historical and current data
   - Merge with player information to add full names

3. **📅 Date Formatting**
   - Convert ranking dates from YYYYMMDD to DD/MM/YYYY format
   - Ensure proper chronological sorting

4. **📈 Pivot Table Creation**
   - Transform data into pivot format
   - Players as rows, dates as columns, points as values
   - Handle missing data with appropriate data types

5. **🖼️ Image Integration**
   - Merge player image URLs
   - Validate image availability for all players

6. **✅ Quality Control & Output**
   - Check for missing player images
   - Sort date columns chronologically
   - Generate final CSV output

## Usage Examples

### Basic Usage

```bash
python data_preparation.py
```

### Expected Output

```python
# If successful:
[DataFrame preview displayed]
Dashboard saved to dashboard.csv

# If players missing images:
There are players without an image ['Player Name 1', 'Player Name 2']
```

## Data Quality & Validation

### Automatic Checks

- ✅ Date format validation
- ✅ Rank range verification (1-10 only)
- ✅ Player image completeness
- ✅ Duplicate entry removal

## Troubleshooting

### Common Issues

**Issue**: Players without images warning

- **Solution**: Add missing player image URLs to `players_images.csv`

### Data Format Requirements

- `atp_rankings_*.csv` expected format

```csv
ranking_date,rank,player,points
20230101,1,104925,11335
20230101,2,104542,6490
```

- `players_images.csv` expected format:

```csv
player_name,player_image_url
Novak Djokovic,https://example.com/djokovic.jpg
Carlos Alcaraz,https://example.com/alcaraz.jpg
```

**Output Size**: dashboard.csv typically ~10KB (estimated based on ~20 players and ~50 date columns)

## Contributing

### Adding New Player Images

1. Add entries to `data/players_images.csv`:

   ```csv
   player_name,player_image_url
   John Malkovich,https://example.com/image.jpg
   ```

### Extending Date Range

- Update `atp_rankings_current.csv` with latest data
- Modify date filter in script if needed: `>= 20230101`

### Code Improvements

- Submit pull requests with clear descriptions
- Follow existing code style and commenting
- Add tests for new functionality

## License

- This project incorporates ATP rankings data (1970-2024) sourced from <https://github.com/JeffSackmann/tennis_atp>, originally licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License by Jeff Sackmann / Tennis Abstract.
- This project, including the script and generated data (e.g., `dashboard.csv`), is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/) by Alessandro Colace. This license requires:
  - **Attribution**: You must give appropriate credit to Alessandro Colace and Jeff Sackmann (for the original data), provide a link to the license, and indicate if changes were made.
  - **NonCommercial**: You may not use this work for commercial purposes.
  - **ShareAlike**: If you remix, transform, or build upon this work, you must distribute your contributions under the same license.
