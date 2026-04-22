import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Define products with shelf life and cost ranges
products = {
    'tomato': {'shelf_life': 72, 'cost_min': 300, 'cost_max': 500},
    'milk': {'shelf_life': 24, 'cost_min': 200, 'cost_max': 300},
    'tilapia': {'shelf_life': 18, 'cost_min': 400, 'cost_max': 600},
    'banana': {'shelf_life': 120, 'cost_min': 100, 'cost_max': 200}
}

# Suppliers
suppliers = ['Supplier A', 'Supplier B', 'Supplier C']

# Generate stock.csv: 120 SKUs
skus = []
sku_id = 1
for product, info in products.items():
    for _ in range(30):  # 30 SKUs per product
        purchased_at = datetime.now() - timedelta(days=random.randint(0, 7))
        quantity = random.randint(50, 200)
        unit_cost = random.uniform(info['cost_min'], info['cost_max'])
        skus.append({
            'sku_id': sku_id,
            'product': product,
            'purchased_at': purchased_at,
            'quantity': quantity,
            'unit_cost_xaf': unit_cost,
            'shelf_life_hours': info['shelf_life'],
            'supplier': random.choice(suppliers)
        })
        sku_id += 1

stock_df = pd.DataFrame(skus)
stock_df.to_csv('data/stock.csv', index=False)

# Generate competitor_prices.csv: 48 hours x 12 stalls x products at 30-min granularity
start_time = datetime.now() - timedelta(hours=48)
timestamps = pd.date_range(start=start_time, end=datetime.now(), freq='30min')
stalls = [f'Stall {i}' for i in range(1, 13)]
comp_prices = []

for ts in timestamps:
    hour = ts.hour
    # Morning premium: 10% higher prices between 6 AM and 12 PM
    premium = 1.1 if 6 <= hour <= 12 else 1.0
    for stall in stalls:
        for product, info in products.items():
            # Daily mean based on product cost range with markup
            daily_mean = (info['cost_min'] + info['cost_max']) / 2 * 1.5
            # Oscillate ±15%
            oscillation = np.random.uniform(-0.15, 0.15)
            price = daily_mean * premium * (1 + oscillation)
            comp_prices.append({
                'timestamp': ts,
                'stall': stall,
                'product': product,
                'price': price
            })

comp_df = pd.DataFrame(comp_prices)
comp_df.to_csv('data/competitor_prices.csv', index=False)

# Generate sales_history.csv: Simulated purchases for demand curve calibration
sales = []
for _ in range(1000):  # Arbitrary number of historical sales
    ts = random.choice(timestamps)
    product = random.choice(list(products.keys()))
    # Simulate prices around cost with markup
    price = random.uniform(products[product]['cost_min'] * 1.2, products[product]['cost_max'] * 1.8)
    qty = random.randint(1, 10)
    sales.append({
        'timestamp': ts,
        'product': product,
        'price': price,
        'quantity': qty
    })

sales_df = pd.DataFrame(sales)
sales_df.to_csv('data/sales_history.csv', index=False)

print("Data generation complete. Files saved in 'data/' directory.")