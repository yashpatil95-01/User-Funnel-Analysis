#!/usr/bin/env python3
"""
Generate static PNG charts for GitHub display
"""

import sys
import os
sys.path.append('src')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.funnel_analyzer import FunnelAnalyzer

# Set style for better looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def generate_static_charts():
    """Generate static charts that display well on GitHub"""
    
    print("Generating static charts for GitHub display...")
    
    # Initialize analyzer and load data
    analyzer = FunnelAnalyzer()
    
    try:
        # Load the sample data
        df = pd.read_csv('data/large_sample_funnel_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"Loaded data: {len(df)} events")
        
        # Process data
        analyzer.data = df
        analyzer.preprocess_data()
        
        # Create funnel analysis
        funnel_steps = ['page_view', 'signup', 'first_purchase', 'repeat_purchase']
        analyzer.create_funnel_analysis(funnel_steps)
        
        # Create output directory
        os.makedirs('outputs/static_charts', exist_ok=True)
        
        # 1. Funnel Conversion Chart
        plt.figure(figsize=(12, 8))
        funnel_data = analyzer.funnel_data
        
        stages = funnel_data['step'].tolist()
        conversions = funnel_data['conversion_rate'].tolist()
        
        bars = plt.bar(stages, conversions, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        plt.title('User Funnel Conversion Rates', fontsize=16, fontweight='bold')
        plt.ylabel('Conversion Rate (%)', fontsize=12)
        plt.xlabel('Funnel Stage', fontsize=12)
        
        # Add value labels on bars
        for bar, conv in zip(bars, conversions):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{conv:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('outputs/static_charts/funnel_conversion_rates.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Traffic Source Performance
        plt.figure(figsize=(10, 6))
        source_data = df.groupby('source').agg({
            'user_id': 'nunique',
            'event': lambda x: (x == 'first_purchase').sum()
        }).reset_index()
        source_data['conversion_rate'] = (source_data['event'] / source_data['user_id']) * 100
        
        bars = plt.bar(source_data['source'], source_data['conversion_rate'], 
                      color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        plt.title('Conversion Rate by Traffic Source', fontsize=16, fontweight='bold')
        plt.ylabel('Conversion Rate (%)', fontsize=12)
        plt.xlabel('Traffic Source', fontsize=12)
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, rate in zip(bars, source_data['conversion_rate']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('outputs/static_charts/source_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Device Performance
        plt.figure(figsize=(8, 6))
        device_data = df.groupby('device').agg({
            'user_id': 'nunique',
            'event': lambda x: (x == 'first_purchase').sum()
        }).reset_index()
        device_data['conversion_rate'] = (device_data['event'] / device_data['user_id']) * 100
        
        bars = plt.bar(device_data['device'], device_data['conversion_rate'],
                      color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
        plt.title('Conversion Rate by Device Type', fontsize=16, fontweight='bold')
        plt.ylabel('Conversion Rate (%)', fontsize=12)
        plt.xlabel('Device Type', fontsize=12)
        
        # Add value labels
        for bar, rate in zip(bars, device_data['conversion_rate']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('outputs/static_charts/device_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Daily Events Trend
        plt.figure(figsize=(12, 6))
        daily_events = df.groupby([df['timestamp'].dt.date, 'event']).size().unstack(fill_value=0)
        
        for event in daily_events.columns:
            plt.plot(daily_events.index, daily_events[event], marker='o', label=event, linewidth=2)
        
        plt.title('Daily Event Trends', fontsize=16, fontweight='bold')
        plt.ylabel('Number of Events', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('outputs/static_charts/daily_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Generated funnel_conversion_rates.png")
        print("✓ Generated source_performance.png") 
        print("✓ Generated device_performance.png")
        print("✓ Generated daily_trends.png")
        print("\nStatic charts saved to outputs/static_charts/")
        
    except Exception as e:
        print(f"Error generating charts: {str(e)}")

if __name__ == "__main__":
    generate_static_charts()