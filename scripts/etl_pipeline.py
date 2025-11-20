import pandas as pd
import json 
import os   

# first
etl_con = os.path.dirname(os.path.abspath(__file__))
os.path.join("folder", "subfolder","file.txt")
print("=" * 60)
print("STEP 1: EXTRACTING DATA FROM SOURCES")
print("=" * 60)

try:
    customers_path = os.path.join(etl_con, 'customer.csv')
    customers = pd.read_csv(customers_path)
    print("\n✅ Customers data loaded successfully")
    print(f"   Shape: {customers.shape}")
    print(f"   Columns: {list(customers.columns)}")
except FileNotFoundError:
    print(f"\n❌ ERROR: File not found at {customers_path}")
    print("💡 TIP: Check that customers.csv exists in the data/ folder")
    exit(1)