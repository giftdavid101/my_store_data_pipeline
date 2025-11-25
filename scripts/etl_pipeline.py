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


# Extract 
try:
    purchases_path = os.path.join(etl_con, 'purchases.json')

    with open(purchases_path, 'r') as file:
        purchase_data = json.load(file)
    purchases = pd.DataFrame(purchase_data)
    print("\n✅ Purchases data loaded successfully!")
    print(f"   Shape: {purchases.shape}")  # Expected: (51, 4)
    print(f"   Columns: {list(purchases.columns)}")
except FileNotFoundError:
    print(f"\n❌ ERROR: File not found at {purchases_path}")
    print("💡 TIP: Check that purchases.json exists in the data/ folder")
    exit(1)
except json.JSONDecodeError:
    print(f"\n❌ ERROR: Invalid JSON syntax in {purchases_path}")
    print("💡 TIP: Validate your JSON at jsonlint.com")
    exit(1)

print("\n" + "=" * 60)
print("DATA PREVIEW")
print("=" * 60)

print("\n📊 First 5 Customers:")
# .head() shows the first 5 rows by default
# .head(10) would show first 10 rows
print(customers.head())

print("\n📊 First 5 Purchases:")
print(purchases.head())

# DATA QUALITY CHECKS

print("\n" + "=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)
customer_duplicates = customers.duplicated().sum()
print(f"\n🔍 Customer duplicates found: {customer_duplicates}")

purchase_duplicates = purchases.duplicated().sum()
print(f"🔍 Purchase duplicates found: {purchase_duplicates}")
print("\n📋 Missing values in customers:")
print(customers.isnull().sum())

print("\n📋 Missing values in purchases:")
print(purchases.isnull().sum())

# Display data types of each column
print("\n📋 Customer data types:")
print(customers.dtypes)

print("\n📋 Purchase data types:")
print(purchases.dtypes)

# STEP 2: Transform Data

print("\n" + "=" * 60)
print("STEP 2: TRANSFORMING DATA")
print("=" * 60)

try:
    # Remove Duplicates
    
    print("\n🧹 Removing duplicates...")
    
    # Count rows before removing duplicates
    customers_before = len(customers)
    purchases_before = len(purchases)
    
    # Remove duplicate rows from customers DataFrame
    # keep='first' means: if duplicates exist, keep the first occurrence
    # inplace=True means: modify the DataFrame directly (don't create a copy)
    customers.drop_duplicates(keep='first', inplace=True)
    
    # Remove duplicate rows from purchases DataFrame
    purchases.drop_duplicates(keep='first', inplace=True)
    
    # Count rows after removing duplicates
    customers_after = len(customers)
    purchases_after = len(purchases)
    
    # Calculate how many duplicates were removed
    customers_removed = customers_before - customers_after
    purchases_removed = purchases_before - purchases_after
    
    # Display results
    print(f"   ✅ Removed {customers_removed} duplicate customer(s)")
    print(f"   ✅ Removed {purchases_removed} duplicate purchase(s)")
    print(f"   📊 Customers now: {customers_after} rows")
    print(f"   📊 Purchases now: {purchases_after} rows")
    
    # 2.2: MERGE DATASETS
    
    print("\n🔗 Merging customers and purchases...")
    
    # Merge (join) the two DataFrames on the 'customer_id' column
    # how='inner' means: only keep rows where customer_id exists in BOTH tables
    # This is like SQL: SELECT * FROM customers INNER JOIN purchases ON customers.customer_id = purchases.customer_id
    merged_data = pd.merge(
        customers,           # Left table
        purchases,           # Right table
        on='customer_id',    # Column to join on
        how='inner'          # Inner join: only matching rows
    )
    
    print(f"   ✅ Merge complete!")
    print(f"   📊 Merged data shape: {merged_data.shape}")
    print(f"   📋 Merged columns: {list(merged_data.columns)}")
    
    # Data Cleaning & Validation
    
    print("\n🧼 Cleaning data...")
    
    # Check for any missing values after merge
    missing_values = merged_data.isnull().sum()
    total_missing = missing_values.sum()
    
    if total_missing > 0:
        print(f"   ⚠️ Found {total_missing} missing values:")
        print(missing_values[missing_values > 0])
        
        # Fill missing amounts with 0
        # In production, you might want to remove these rows instead
        merged_data['amount'].fillna(0, inplace=True)
        print("   ✅ Filled missing amounts with 0")
    else:
        print("   ✅ No missing values detected!")
    
    # Remove any rows with negative amounts (data quality issue)
    # In real e-commerce, negative amounts might indicate refunds
    negative_amounts = (merged_data['amount'] < 0).sum()
    if negative_amounts > 0:
        print(f"   ⚠️ Found {negative_amounts} negative amounts (removing them)")
        merged_data = merged_data[merged_data['amount'] >= 0]
    else:
        print("   ✅ No negative amounts found")
    
    # 2.4: DATA ENRICHMENT
    
    print("\n💰 Enriching data with currency conversion...")
    
    # Add a new column: convert Nigerian Naira to USD
    # Exchange rate: 1 NGN = 0.0012 USD (as of 2024)
    # This makes data comparable to international standards
    merged_data['amount_usd'] = (merged_data['amount'] * 0.0012).round(2)
    
    print("   ✅ Added 'amount_usd' column")
    
    # Add a new column: categorize purchase amounts
    # This helps with analysis and segmentation
    def categorize_purchase(amount):
        if amount < 15000:
            return 'Low'
        elif amount < 30000:
            return 'Medium'
        else:
            return 'High'
    
    # Apply the function to each row
    # .apply() runs the function on every value in the 'amount' column
    merged_data['purchase_category'] = merged_data['amount'].apply(categorize_purchase)
    
    print("   ✅ Added 'purchase_category' column")
    
    # 2.5: FINAL VALIDATION
    
    print("\n✓ Running final validation checks...")
    
    # Check 1: Ensure no duplicates in merged data
    final_duplicates = merged_data.duplicated().sum()
    print(f"   ✓ Duplicates in merged data: {final_duplicates}")
    
    # Check 2: Ensure all amounts are positive
    all_positive = (merged_data['amount'] >= 0).all()
    print(f"   ✓ All amounts are positive: {all_positive}")
    
    # Check 3: Ensure USD conversion worked
    has_usd = 'amount_usd' in merged_data.columns
    print(f"   ✓ USD column exists: {has_usd}")
    
    # Check 4: Verify data types
    correct_types = (
        merged_data['customer_id'].dtype == 'int64' and
        merged_data['amount'].dtype == 'int64' and
        merged_data['amount_usd'].dtype == 'float64'
    )
    print(f"   ✓ Data types are correct: {correct_types}")
    
    # DISPLAY TRANSFORMED DATA PREVIEW
    print("\n" + "=" * 60)
    print("TRANSFORMED DATA PREVIEW")
    print("=" * 60)
    
    # Show first 10 rows of transformed data
    print("\n📊 First 10 rows of merged data:")
    print(merged_data.head(10))
    
    # Show summary statistics
    print("\n📈 Summary Statistics:")
    # .describe() shows count, mean, std, min, max, quartiles
    print(merged_data[['amount', 'amount_usd']].describe())
    
    # Show value counts for purchase categories
    print("\n📊 Purchase Category Distribution:")
    # .value_counts() counts occurrences of each unique value
    print(merged_data['purchase_category'].value_counts())
    
except KeyError as e:
    # KeyError occurs when trying to access a column that doesn't exist
    print(f"\n❌ ERROR: Missing expected column - {e}")
    print("💡 TIP: Check that your CSV/JSON have the correct column names")
    exit(1)
    
except Exception as e:
    # Catch any other unexpected errors
    print(f"\n❌ ERROR: Unexpected error during transformation - {e}")
    exit(1)

# Add email domain extration
merged_data['email_domain'] = merged_data['email'].str.split('@').str[1]
print("✅ Added 'email_domain' column")

# Step 3: Load data to Postgresql

print("\n" + "=" * 60)
print("STEP 3: LOADING DATA TO POSTGRESQL")
print("=" * 60)

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

try:
    #Create database connection
    print("\n🔌 Connecting to PostgreSQL database...")



    # configuration
    DB_USER = os.getenv('DB_USER')               # Your PostgreSQL username
    DB_PASSWORD = os.getenv('DB_PASSWORD')           # Your PostgreSQL password
    DB_HOST = os.getenv('DB_HOST')            # Database server (localhost for local)
    DB_PORT = os.getenv('DB_PORT')                    # PostgreSQL default port
    DB_NAME = os.getenv('DB_NAME')

    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    #test the connection
    with engine.connect() as connection:
        print("   ✅ Database connection successful!")

    # Load data to table
    print("\n💾 Loading data to 'sales_data' table...")
    merged_data.to_sql(
        'sales_data',           # Table name
        engine,                 # Database connection
        if_exists='replace',    # Drop and recreate if exists
        index=False             # Don't include DataFrame index
    )
    print(f"   ✅ Data loaded successfully!")
    print(f"   📊 Table: sales_data")
    print(f"   📊 Rows loaded: {len(merged_data)}")
    print(f"   📊 Columns: {len(merged_data.columns)}")

    # verify data was loaded by querying
    print("\n🔍 Verifying data in database...")

    query = "SELECT COUNT(*) as row_count FROM sales_data;"
    result = pd.read_sql(query, engine)

    print(f"   ✅ Rows in database: {result['row_count'][0]}")

    # Close the database connection
    engine.dispose()
    print("   ✅ Database connection closed")




 


except    