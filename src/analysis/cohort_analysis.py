import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from operator import attrgetter

class CohortAnalyzer:
    def __init__(self, data):
        self.data = data
        self.cohort_data = None
    
    def create_cohort_analysis(self, user_col='user_id', timestamp_col='timestamp', event_col='event'):
        """Create cohort analysis based on user first event date"""
        
        # Get first event date for each user (cohort assignment)
        user_first_event = self.data.groupby(user_col)[timestamp_col].min().reset_index()
        user_first_event.columns = [user_col, 'cohort_date']
        user_first_event['cohort_period'] = user_first_event['cohort_date'].dt.to_period('M')
        
        # Merge back with original data
        cohort_data = self.data.merge(user_first_event, on=user_col)
        
        # Calculate period number (months since first event)
        cohort_data['event_period'] = cohort_data[timestamp_col].dt.to_period('M')
        cohort_data['period_number'] = (
            cohort_data['event_period'] - cohort_data['cohort_period']
        ).apply(attrgetter('n'))
        
        # Create cohort table
        cohort_table = cohort_data.groupby(['cohort_period', 'period_number'])[user_col].nunique().reset_index()
        cohort_table = cohort_table.pivot(index='cohort_period', 
                                         columns='period_number', 
                                         values=user_col)
        
        # Calculate retention rates
        cohort_sizes = cohort_table.iloc[:, 0]
        retention_table = cohort_table.divide(cohort_sizes, axis=0)
        
        self.cohort_data = {
            'cohort_table': cohort_table,
            'retention_table': retention_table,
            'cohort_sizes': cohort_sizes
        }
        
        return self.cohort_data
    
    def plot_cohort_heatmap(self):
        """Create cohort retention heatmap"""
        if self.cohort_data is None:
            print("No cohort data available. Run create_cohort_analysis first.")
            return
        
        retention_table = self.cohort_data['retention_table']
        
        fig = go.Figure(data=go.Heatmap(
            z=retention_table.values,
            x=[f'Period {i}' for i in retention_table.columns],
            y=[str(idx) for idx in retention_table.index],
            colorscale='Blues',
            text=np.round(retention_table.values * 100, 1),
            texttemplate='%{text}%',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Cohort Retention Analysis',
            xaxis_title='Period Number',
            yaxis_title='Cohort Month',
            height=500
        )
        
        return fig
    
    def plot_retention_curves(self):
        """Plot retention curves for different cohorts"""
        if self.cohort_data is None:
            print("No cohort data available.")
            return
        
        retention_table = self.cohort_data['retention_table']
        
        fig = go.Figure()
        
        for cohort in retention_table.index:
            fig.add_trace(go.Scatter(
                x=retention_table.columns,
                y=retention_table.loc[cohort] * 100,
                mode='lines+markers',
                name=str(cohort),
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title='Retention Curves by Cohort',
            xaxis_title='Period Number',
            yaxis_title='Retention Rate (%)',
            height=500,
            hovermode='x unified'
        )
        
        return fig