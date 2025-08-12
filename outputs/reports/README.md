# Outputs Directory

This directory contains generated analysis results, visualizations, and reports.

## Main Output Structure

- `charts/` — All static and interactive chart outputs:
	- `funnel_chart.png` — Funnel chart (static image)
	- `conversion_rates.png` — Conversion rates chart (static image)
	- `daily_trends.png` — Daily event trends (static image)
	- `journey_length_distribution.png` — User journey length distribution (static image)
	- `funnel_chart.html` — Interactive funnel visualization
	- `conversion_rates.html` — Interactive conversion rate chart

- `data_exports/` — Exported CSVs for further analysis:
	- `daily_events.csv`, `device_performance.csv`, `funnel_metrics.csv`, `journey_length_distribution.csv`, `source_performance.csv`

- `reports/` — Text and summary reports:
	- `analysis_summary.txt` — Key findings and summary
	- `README.md` — This file

- Other outputs:
	- `funnel_chart.html`, `conversion_rates.html` (legacy, also in charts/)
	- `device_performance.csv`, `funnel_metrics.csv`, `journey_length_distribution.csv`, `source_performance.csv` (also in data_exports/)

## File Types
- `.html` — Interactive visualizations (open in browser)
- `.png` — Static chart images
- `.csv` — Raw/exported data
- `.txt` — Text summary reports