import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_large_sample_data(num_users=10000, output_path='data/large_sample_funnel_data.csv'):
    """Generate a large sample dataset with 10k users for funnel analysis"""
    
    np.random.seed(42)
    events = []
    sources = ['organic', 'paid', 'social', 'email', 'direct']
    devices = ['desktop', 'mobile', 'tablet']
    
    print(f"Generating sample data for {num_users} users...")
    
    for user in range(1, num_users + 1):
        if user % 1000 == 0:
            print(f"Processing user {user}/{num_users}")
            
        # Random user attributes
        source = np.random.choice(sources, p=[0.35, 0.25, 0.20, 0.15, 0.05])  # Weighted probabilities
        device = np.random.choice(devices, p=[0.45, 0.40, 0.15])  # Desktop, mobile, tablet
        start_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 90))
        
        # Each user starts with page_view
        events.append({
            'user_id': user,
            'event': 'page_view',
            'timestamp': start_date,
            'source': source,
            'device': device
        })
        
        # 65% proceed to signup (varies by source)
        signup_rate = {
            'organic': 0.70,
            'paid': 0.75,
            'social': 0.60,
            'email': 0.80,
            'direct': 0.65
        }
        
        if np.random.random() < signup_rate[source]:
            events.append({
                'user_id': user,
                'event': 'signup',
                'timestamp': events[-1]['timestamp'] + pd.Timedelta(minutes=np.random.randint(1, 120)),
                'source': source,
                'device': device
            })
            
            # 35% of signups make first purchase (varies by device)
            purchase_rate = {
                'desktop': 0.40,
                'mobile': 0.30,
                'tablet': 0.35
            }
            
            if np.random.random() < purchase_rate[device]:
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
    
    # Create DataFrame
    df = pd.DataFrame(events)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"\nSample data generated successfully!")
    print(f"Total events: {len(df):,}")
    print(f"Unique users: {df['user_id'].nunique():,}")
    print(f"File saved to: {output_path}")
    print(f"\nEvent distribution:")
    print(df['event'].value_counts())
    print(f"\nSource distribution:")
    print(df['source'].value_counts())
    print(f"\nDevice distribution:")
    print(df['device'].value_counts())
    
    return df

if __name__ == "__main__":
    # Generate the large sample dataset
    df = generate_large_sample_data(10000)