import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from funnel_analyzer import FunnelAnalyzer

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for demonstration
def create_sample_data():
    """Create sample funnel data for demonstration - 10k users"""
    import numpy as np
    np.random.seed(42)
    
    # Simulate user journey data for 10,000 users
    users = range(1, 10001)
    events = []
    sources = ['organic', 'paid', 'social', 'email', 'direct']
    devices = ['desktop', 'mobile', 'tablet']
    
    for user in users:
        # Random user attributes
        source = np.random.choice(sources)
        device = np.random.choice(devices)
        start_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 90))
        
        # Each user starts with page_view
        events.append({
            'user_id': user,
            'event': 'page_view',
            'timestamp': start_date,
            'source': source,
            'device': device
        })
        
        # 65% proceed to signup (realistic conversion)
        if np.random.random() < 0.65:
            events.append({
                'user_id': user,
                'event': 'signup',
                'timestamp': events[-1]['timestamp'] + pd.Timedelta(minutes=np.random.randint(1, 120)),
                'source': source,
                'device': device
            })
            
            # 35% of signups make first purchase
            if np.random.random() < 0.35:
                events.append({
                    'user_id': user,
                    'event': 'first_purchase',
                    'timestamp': events[-1]['timestamp'] + pd.Timedelta(hours=np.random.randint(1, 72)),
                    'source': source,
                    'device': device
                })
                
                # 30% make repeat purchase
                if np.random.random() < 0.30:
                    events.append({
                        'user_id': user,
                        'event': 'repeat_purchase',
                        'timestamp': events[-1]['timestamp'] + pd.Timedelta(days=np.random.randint(1, 21)),
                        'source': source,
                        'device': device
                    })
                    
                    # 20% become loyal customers (3+ purchases)
                    if np.random.random() < 0.20:
                        for i in range(np.random.randint(1, 4)):
                            events.append({
                                'user_id': user,
                                'event': 'repeat_purchase',
                                'timestamp': events[-1]['timestamp'] + pd.Timedelta(days=np.random.randint(7, 30)),
                                'source': source,
                                'device': device
                            })
    
    return pd.DataFrame(events)

# Initialize analyzer with sample data
analyzer = FunnelAnalyzer()
sample_data = create_sample_data()
analyzer.data = sample_data
analyzer.preprocess_data()

funnel_steps = ['page_view', 'signup', 'first_purchase', 'repeat_purchase']
analyzer.create_funnel_analysis(funnel_steps)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("User Funnel Analysis Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Funnel Overview", className="card-title"),
                    dcc.Graph(
                        id='funnel-chart',
                        figure=analyzer.plot_funnel_chart()
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Conversion Rates", className="card-title"),
                    dcc.Graph(
                        id='conversion-chart',
                        figure=analyzer.plot_conversion_rates()
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Funnel Metrics Summary", className="card-title"),
                    html.Div(id='metrics-table')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Key Insights", className="card-title"),
                    html.Div(id='insights')
                ])
            ])
        ], width=6)
    ])
], fluid=True)

@callback(
    Output('metrics-table', 'children'),
    Input('funnel-chart', 'figure')
)
def update_metrics_table(figure):
    """Update the metrics summary table"""
    if analyzer.funnel_data is None:
        return "No data available"
    
    table_data = []
    for _, row in analyzer.funnel_data.iterrows():
        table_data.append(
            html.Tr([
                html.Td(row['step']),
                html.Td(f"{row['count']:,}"),
                html.Td(f"{row['conversion_rate']:.1f}%"),
                html.Td(f"{row['step_conversion']:.1f}%")
            ])
        )
    
    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Step"),
                html.Th("Users"),
                html.Th("Overall Rate"),
                html.Th("Step Rate")
            ])
        ]),
        html.Tbody(table_data)
    ], striped=True, bordered=True, hover=True)

@callback(
    Output('insights', 'children'),
    Input('funnel-chart', 'figure')
)
def update_insights(figure):
    """Generate key insights from the funnel data"""
    if analyzer.funnel_data is None:
        return "No insights available"
    
    insights = []
    
    # Find biggest drop-off
    step_drops = []
    for i in range(1, len(analyzer.funnel_data)):
        drop = analyzer.funnel_data.iloc[i-1]['step_conversion'] - analyzer.funnel_data.iloc[i]['step_conversion']
        step_drops.append((analyzer.funnel_data.iloc[i]['step'], drop))
    
    biggest_drop = max(step_drops, key=lambda x: x[1])
    
    insights.extend([
        html.P(f"📉 Biggest drop-off: {biggest_drop[0]} ({biggest_drop[1]:.1f}% loss)", className="mb-2"),
        html.P(f"🎯 Overall conversion rate: {analyzer.funnel_data.iloc[-1]['conversion_rate']:.1f}%", className="mb-2"),
        html.P(f"👥 Total users in funnel: {analyzer.funnel_data.iloc[0]['count']:,}", className="mb-2"),
        html.P(f"✅ Final conversions: {analyzer.funnel_data.iloc[-1]['count']:,}", className="mb-2")
    ])
    
    return insights

if __name__ == '__main__':
    app.run_server(debug=True)