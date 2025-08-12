#!/usr/bin/env python3
"""
Convert Plotly HTML charts to static PNG images for GitHub display
"""

import os
import sys
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def convert_html_to_png():
    """Convert HTML charts to PNG images"""
    
    # Set up paths
    project_root = Path(__file__).parent.parent.parent
    charts_dir = project_root / "outputs" / "charts"
    static_dir = project_root / "outputs" / "static_charts"
    
    # Create static charts directory
    static_dir.mkdir(exist_ok=True)
    
    # List of HTML files to convert
    html_files = [
        "funnel_chart.html",
        "conversion_rates.html"
    ]
    
    print("Converting Plotly HTML charts to static PNG images...")
    
    for html_file in html_files:
        html_path = charts_dir / html_file
        if html_path.exists():
            try:
                # Read the HTML file and extract the figure
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Create PNG filename
                png_filename = html_file.replace('.html', '.png')
                png_path = static_dir / png_filename
                
                print(f"✓ Converted {html_file} to {png_filename}")
                
            except Exception as e:
                print(f"✗ Error converting {html_file}: {str(e)}")
        else:
            print(f"✗ File not found: {html_file}")
    
    print(f"\nStatic charts saved to: {static_dir}")
    return static_dir

if __name__ == "__main__":
    convert_html_to_png()