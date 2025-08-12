"""
Export Results Script
Run this script to generate and save all analysis results to the outputs folder
"""

import sys
import os
sys.path.append('.')

from funnel_analyzer import FunnelAnalyzer
from cohort_analysis import CohortAnalyzer
import pandas as pd
import numpy as np

def main():
    print("🚀 Starting Funnel Analysis Export...")
    
    # Initialize analyzer
    analyzer = FunnelAnalyzer()
    
    # Load the large sample data
    try:
        analyzer.load_data('data/large_sample_funnel_data.csv')
        print("✅ Data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print("💡 Run 'python src/generate_sample_data.py' first to create sample data")
        return
    
    # Preprocess data
    analyzer.preprocess_data()
    
    # Define funnel steps
    funnel_steps = ['page_view', 'signup', 'first_purchase', 'repeat_purchase']
    
    # Create funnel analysis
    print("📊 Creating funnel analysis...")
    funnel_data = analyzer.create_funnel_analysis(funnel_steps)
    print(funnel_data)
    
    # Save all visualizations
    print("💾 Saving visualizations...")
    analyzer.save_visualizations('outputs')
    
    # Create additional analysis
    print("📈 Creating additional analysis...")
    
    # Source performance analysis
    source_analysis = analyzer.data.groupby(['source', 'event']).size().unstack(fill_value=0)
    if 'first_purchase' in source_analysis.columns and 'page_view' in source_analysis.columns:
        source_analysis['conversion_rate'] = (source_analysis['first_purchase'] / source_analysis['page_view'] * 100).round(2)
    source_analysis.to_csv('outputs/source_performance.csv')
    
    # Device performance analysis
    device_analysis = analyzer.data.groupby(['device', 'event']).size().unstack(fill_value=0)
    if 'first_purchase' in device_analysis.columns and 'page_view' in device_analysis.columns:
        device_analysis['conversion_rate'] = (device_analysis['first_purchase'] / device_analysis['page_view'] * 100).round(2)
    device_analysis.to_csv('outputs/device_performance.csv')
    
    # Time-based analysis
    analyzer.data['date'] = analyzer.data['timestamp'].dt.date
    daily_events = analyzer.data.groupby(['date', 'event']).size().unstack(fill_value=0)
    daily_events.to_csv('outputs/daily_events.csv')
    
    # User journey analysis
    user_journeys = analyzer.data.groupby('user_id')['event'].apply(list).reset_index()
    user_journeys['journey_length'] = user_journeys['event'].apply(len)
    journey_summary = user_journeys['journey_length'].value_counts().sort_index()
    journey_summary.to_csv('outputs/journey_length_distribution.csv')
    
    # Create summary report
    create_summary_report(analyzer, funnel_data, source_analysis, device_analysis)
    
    print("\n🎉 Analysis complete! Results saved to outputs/ folder:")
    print("📁 Check the outputs/ directory for:")
    print("   - Interactive HTML charts")
    print("   - CSV data exports")
    print("   - Summary report")

def create_summary_report(analyzer, funnel_data, source_analysis, device_analysis):
    """Create a text summary report"""
    
    report = []
    report.append("=" * 60)
    report.append("USER FUNNEL ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Events: {len(analyzer.data):,}")
    report.append(f"Unique Users: {analyzer.data['user_id'].nunique():,}")
    report.append("")
    
    report.append("FUNNEL PERFORMANCE:")
    report.append("-" * 30)
    for _, row in funnel_data.iterrows():
        report.append(f"{row['step']:<20} {row['count']:>8,} users ({row['conversion_rate']:>5.1f}%)")
    report.append("")
    
    report.append("TOP PERFORMING SOURCES:")
    report.append("-" * 30)
    if 'conversion_rate' in source_analysis.columns:
        top_sources = source_analysis.nlargest(3, 'conversion_rate')
        for source, row in top_sources.iterrows():
            report.append(f"{source:<15} {row['conversion_rate']:>5.1f}% conversion")
    report.append("")
    
    report.append("DEVICE PERFORMANCE:")
    report.append("-" * 30)
    if 'conversion_rate' in device_analysis.columns:
        for device, row in device_analysis.iterrows():
            report.append(f"{device:<15} {row['conversion_rate']:>5.1f}% conversion")
    report.append("")
    
    report.append("KEY INSIGHTS:")
    report.append("-" * 30)
    
    # Calculate biggest drop-off
    step_drops = []
    for i in range(1, len(funnel_data)):
        drop = funnel_data.iloc[i-1]['step_conversion'] - funnel_data.iloc[i]['step_conversion']
        step_drops.append((funnel_data.iloc[i]['step'], drop))
    
    if step_drops:
        biggest_drop = max(step_drops, key=lambda x: x[1])
        report.append(f"• Biggest drop-off at: {biggest_drop[0]} ({biggest_drop[1]:.1f}% loss)")
    
    report.append(f"• Overall conversion rate: {funnel_data.iloc[-1]['conversion_rate']:.1f}%")
    report.append(f"• {funnel_data.iloc[-1]['count']:,} users completed the full funnel")
    
    # Save report
    with open('outputs/analysis_summary.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("📄 Summary report saved to outputs/analysis_summary.txt")

if __name__ == "__main__":
    main()