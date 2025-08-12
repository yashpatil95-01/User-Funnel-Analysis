# User Funnel Analysis Project

A comprehensive data analysis project for analyzing user conversion funnels with interactive visualizations.

## Features

- Data preprocessing and cleaning
- Funnel conversion rate analysis
- Interactive visualizations with Plotly
- Statistical significance testing
- Cohort analysis
- Time-based funnel trends

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your funnel data in the `data/` directory
3. Run the analysis:
```bash
python src/funnel_analyzer.py
```

## Project Structure

```
user-funnel-analysis/
├── data/                 # Raw and processed data
├── src/                  # Source code
├── notebooks/            # Jupyter notebooks for exploration
├── outputs/              # Generated reports and visualizations
└── config/               # Configuration files
```

## Data Format

Expected CSV format with columns:
- user_id: Unique user identifier
- event: Funnel step name
- timestamp: Event timestamp
- source: Traffic source (organic, paid, social, email, direct)
- device: Device type (desktop, mobile, tablet)

## Sample Data

The project includes a large sample dataset with 10,000 users and ~20k events:
- Run `python src/generate_sample_data.py` to create fresh sample data
- Pre-generated sample available in `data/large_sample_funnel_data.csv`