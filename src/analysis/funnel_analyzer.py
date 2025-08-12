import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class FunnelAnalyzer:
    def __init__(self, data_path=None):
        self.data = None
        self.funnel_data = None
        self.conversion_rates = None
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path):
        """Load funnel data from CSV file"""
        try:
            self.data = pd.read_csv(data_path)
            print(f"Data loaded successfully: {len(self.data)} rows")
            print(f"Columns: {list(self.data.columns)}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def preprocess_data(self, timestamp_col='timestamp', user_col='user_id', event_col='event'):
        """Clean and preprocess the funnel data"""
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        # Convert timestamp to datetime
        self.data[timestamp_col] = pd.to_datetime(self.data[timestamp_col])
        
        # Sort by user and timestamp
        self.data = self.data.sort_values([user_col, timestamp_col])
        
        # Remove duplicates
        self.data = self.data.drop_duplicates(subset=[user_col, event_col])
        
        print("Data preprocessing completed")
        return self.data
    
    def create_funnel_analysis(self, funnel_steps, user_col='user_id', event_col='event'):
        """Create funnel analysis with conversion rates"""
        if self.data is None:
            print("No data available for analysis")
            return
        
        funnel_results = []
        
        for i, step in enumerate(funnel_steps):
            if i == 0:
                # First step - all users who performed this event
                users_at_step = set(self.data[self.data[event_col] == step][user_col])
                total_users = len(users_at_step)
            else:
                # Subsequent steps - users who performed previous step AND this step
                prev_users = funnel_results[i-1]['users']
                current_step_users = set(self.data[self.data[event_col] == step][user_col])
                users_at_step = prev_users.intersection(current_step_users)
                total_users = len(users_at_step)
            
            # Calculate conversion rate
            if i == 0:
                conversion_rate = 100.0
                step_conversion = 100.0
            else:
                conversion_rate = (total_users / funnel_results[0]['count']) * 100
                step_conversion = (total_users / funnel_results[i-1]['count']) * 100
            
            funnel_results.append({
                'step': step,
                'count': total_users,
                'conversion_rate': conversion_rate,
                'step_conversion': step_conversion,
                'users': users_at_step
            })
        
        self.funnel_data = pd.DataFrame([
            {
                'step': r['step'],
                'count': r['count'],
                'conversion_rate': r['conversion_rate'],
                'step_conversion': r['step_conversion']
            }
            for r in funnel_results
        ])
        
        return self.funnel_data
    
    def plot_funnel_chart(self, title="User Conversion Funnel"):
        """Create an interactive funnel visualization"""
        if self.funnel_data is None:
            print("No funnel data available. Run create_funnel_analysis first.")
            return
        
        fig = go.Figure()
        
        # Funnel chart
        fig.add_trace(go.Funnel(
            y=self.funnel_data['step'],
            x=self.funnel_data['count'],
            textinfo="value+percent initial+percent previous",
            texttemplate="<b>%{y}</b><br>Users: %{value}<br>Overall: %{percentInitial}<br>Step: %{percentPrevious}",
            connector={"line": {"color": "royalblue", "dash": "solid", "width": 3}},
            marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
                   "line": {"width": [4, 2, 2, 3, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        ))
        
        fig.update_layout(
            title=title,
            font_size=12,
            height=600
        )
        
        return fig
    
    def plot_conversion_rates(self):
        """Plot conversion rates at each step"""
        if self.funnel_data is None:
            print("No funnel data available.")
            return
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Overall Conversion Rate', 'Step-by-Step Conversion Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Overall conversion rates
        fig.add_trace(
            go.Bar(
                x=self.funnel_data['step'],
                y=self.funnel_data['conversion_rate'],
                name='Overall Conversion',
                marker_color='lightblue',
                text=[f"{rate:.1f}%" for rate in self.funnel_data['conversion_rate']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # Step conversion rates
        fig.add_trace(
            go.Bar(
                x=self.funnel_data['step'],
                y=self.funnel_data['step_conversion'],
                name='Step Conversion',
                marker_color='lightcoral',
                text=[f"{rate:.1f}%" for rate in self.funnel_data['step_conversion']],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Funnel Conversion Analysis",
            height=500,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=2)
        
        return fig
    
    def save_visualizations(self, output_dir='outputs'):
        """Save all visualizations to the outputs directory"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if self.funnel_data is None:
            print("No funnel data available. Run create_funnel_analysis first.")
            return
        
        # Save funnel chart
        funnel_chart = self.plot_funnel_chart()
        funnel_chart.write_html(f"{output_dir}/funnel_chart.html")
        try:
            funnel_chart.write_image(f"{output_dir}/funnel_chart.png", width=1200, height=800)
        except Exception as e:
            print(f"Note: Could not save PNG (install kaleido for image export): {e}")
        
        # Save conversion rates chart
        conversion_chart = self.plot_conversion_rates()
        conversion_chart.write_html(f"{output_dir}/conversion_rates.html")
        try:
            conversion_chart.write_image(f"{output_dir}/conversion_rates.png", width=1200, height=600)
        except Exception as e:
            print(f"Note: Could not save PNG (install kaleido for image export): {e}")
        
        # Save metrics summary
        self.funnel_data.to_csv(f"{output_dir}/funnel_metrics.csv", index=False)
        
        print(f"Visualizations saved to {output_dir}/ directory:")
        print("- funnel_chart.html (interactive)")
        print("- conversion_rates.html (interactive)")
        print("- funnel_metrics.csv (data export)")
        
        return True

if __name__ == "__main__":
    # Example usage
    analyzer = FunnelAnalyzer()
    
    # Load sample data (you'll need to provide your own data file)
    # analyzer.load_data('../data/funnel_data.csv')
    # analyzer.preprocess_data()
    
    # Define your funnel steps
    # funnel_steps = ['page_view', 'signup', 'first_purchase', 'repeat_purchase']
    # analyzer.create_funnel_analysis(funnel_steps)
    
    # Generate visualizations
    # funnel_chart = analyzer.plot_funnel_chart()
    # funnel_chart.show()
    
    # conversion_chart = analyzer.plot_conversion_rates()
    # conversion_chart.show()
    
    # Save visualizations
    # analyzer.save_visualizations()
    
    print("Funnel Analyzer initialized. Load your data to begin analysis.")