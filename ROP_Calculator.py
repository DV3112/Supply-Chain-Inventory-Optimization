import pandas as pd
import numpy as np

# ==========================================
# 1. DATA SIMULATION
# ==========================================
# Generating 30 days of mock historical sales data for 3 products
np.random.seed(42)

data = {
    'Date': pd.date_range(start='2026-01-01', periods=30),
    'Product_A_Sales': np.random.normal(loc=50, scale=5, size=30).astype(int),
    'Product_B_Sales': np.random.normal(loc=20, scale=12, size=30).astype(int),
    'Product_C_Sales': np.random.normal(loc=150, scale=25, size=30).astype(int)
}
df = pd.DataFrame(data)

# Ensure no negative sales days
products = ['Product_A_Sales', 'Product_B_Sales', 'Product_C_Sales']
df[products] = df[products].clip(lower=0)

# ==========================================
# 2. SUPPLY CHAIN CONSTANTS
# ==========================================
lead_time_days = 7
z_score = 1.65 # 95% Service Level

print("--- SUPPLY CHAIN INVENTORY OPTIMIZATION MODEL ---\n")
print(f"Assumptions: {lead_time_days}-Day Lead Time | 95% Service Level Target\n")

# ==========================================
# 3. CALCULATE REORDER POINTS (ROP)
# ==========================================

for product in products:
    # A. Average Daily Demand
    avg_daily_demand = df[product].mean()

    # B. Demand Volatility (Standard Deviation)
    std_dev_demand = df[product].std()

    # C. Safety Stock
    safety_stock = z_score * std_dev_demand * np.sqrt(lead_time_days)

    # D. Reorder Point (ROP)
    reorder_point = (avg_daily_demand * lead_time_days) + safety_stock

    # Output
    product_name = product.replace('_Sales', '')
    print(f"[{product_name}] Analysis:")
    print(f"  > Avg Daily Demand:  {avg_daily_demand:.0f} units")
    print(f"  > Demand Volatility: {std_dev_demand:.0f} units (Std Dev)")
    print(f"  > Safety Stock:      {safety_stock:.0f} units required")
    print(f"  > REORDER POINT:     Trigger new PO when inventory drops to {reorder_point:.0f} units\n")
