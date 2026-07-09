# ==========================================================
# Quantium Virtual Internship
# Task 1 - Data Preparation & Customer Analytics
# Author : Syed Ubedullah Basha
# ==========================================================

# ==========================================================
# Import Libraries
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# Load Datasets
# ==========================================================

transaction_data = pd.read_excel("QVI_transaction_data.xlsx")

purchase_behaviour = pd.read_csv("QVI_purchase_behaviour.csv")

print("="*60)
print("Datasets Loaded Successfully")
print("="*60)

# ==========================================================
# Display First 5 Rows
# ==========================================================

print("\nTransaction Data")
print(transaction_data.head())

print("\nPurchase Behaviour")
print(purchase_behaviour.head())

# ==========================================================
# Dataset Shape
# ==========================================================

print("\nTransaction Shape:")
print(transaction_data.shape)

print("\nPurchase Behaviour Shape:")
print(purchase_behaviour.shape)

# ==========================================================
# Column Names
# ==========================================================

print("\nTransaction Columns")
print(transaction_data.columns)

print("\nPurchase Behaviour Columns")
print(purchase_behaviour.columns)

# ==========================================================
# Dataset Information
# ==========================================================

print("\nTransaction Information")
transaction_data.info()

print("\nPurchase Behaviour Information")
purchase_behaviour.info()

# ==========================================================
# Statistical Summary
# ==========================================================

print("\nTransaction Summary")
print(transaction_data.describe())

print("\nPurchase Behaviour Summary")
print(purchase_behaviour.describe())

# ==========================================================
# Missing Values
# ==========================================================

print("\nMissing Values in Transaction Data")
print(transaction_data.isnull().sum())

print("\nMissing Values in Purchase Behaviour")
print(purchase_behaviour.isnull().sum())

# ==========================================================
# Duplicate Rows
# ==========================================================

print("\nDuplicate Rows in Transaction Data")
print(transaction_data.duplicated().sum())

print("\nDuplicate Rows in Purchase Behaviour")
print(purchase_behaviour.duplicated().sum())

# ==========================================================
# Convert Date
# ==========================================================

transaction_data["DATE"] = pd.to_datetime(
    transaction_data["DATE"],
    origin="1899-12-30",
    unit="D"
)

print("\nDate Converted Successfully")

# ==========================================================
# Check Data Types
# ==========================================================

print("\nData Types")
print(transaction_data.dtypes)

# ==========================================================
# Remove Duplicate Rows
# ==========================================================

transaction_data = transaction_data.drop_duplicates()

purchase_behaviour = purchase_behaviour.drop_duplicates()

print("\nDuplicates Removed")

# ==========================================================
# Remove Missing Values
# ==========================================================

transaction_data = transaction_data.dropna()

purchase_behaviour = purchase_behaviour.dropna()

print("\nMissing Values Removed")

# ==========================================================
# Check Quantity
# ==========================================================

print("\nMinimum Quantity")
print(transaction_data["PROD_QTY"].min())

print("\nMaximum Quantity")
print(transaction_data["PROD_QTY"].max())

# ==========================================================
# Check Sales
# ==========================================================

print("\nMinimum Sales")
print(transaction_data["TOT_SALES"].min())

print("\nMaximum Sales")
print(transaction_data["TOT_SALES"].max())

# ==========================================================
# Remove Negative Values (if any)
# ==========================================================

transaction_data = transaction_data[
    transaction_data["PROD_QTY"] > 0
]

transaction_data = transaction_data[
    transaction_data["TOT_SALES"] > 0
]

print("\nNegative Values Removed")

# ==========================================================
# Final Shape
# ==========================================================

print("\nFinal Transaction Shape")
print(transaction_data.shape)

print("\nFinal Purchase Behaviour Shape")
print(purchase_behaviour.shape)

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

print("\n" + "="*60)
print("FEATURE ENGINEERING")
print("="*60)

# -----------------------------
# Extract Pack Size
# -----------------------------
transaction_data["PACK_SIZE"] = transaction_data["PROD_NAME"].str.extract(r'(\d+)g')
transaction_data["PACK_SIZE"] = transaction_data["PACK_SIZE"].astype(float)

print("\nPack Size Extracted Successfully")

# -----------------------------
# Extract Brand Name
# -----------------------------
transaction_data["BRAND"] = transaction_data["PROD_NAME"].str.split().str[0]

print("\nBrand Name Extracted Successfully")

# Check first few rows
print(transaction_data[["PROD_NAME","BRAND","PACK_SIZE"]].head())

# ==========================================================
# MERGE BOTH DATASETS
# ==========================================================

merged_data = pd.merge(
    transaction_data,
    purchase_behaviour,
    on="LYLTY_CARD_NBR",
    how="left"
)

print("\nDatasets Merged Successfully")

print("\nMerged Dataset Shape")
print(merged_data.shape)

# ==========================================================
# SALES METRICS
# ==========================================================

print("\n" + "="*60)
print("SALES METRICS")
print("="*60)

total_sales = merged_data["TOT_SALES"].sum()

total_transactions = merged_data["TXN_ID"].nunique()

total_customers = merged_data["LYLTY_CARD_NBR"].nunique()

average_transaction = merged_data["TOT_SALES"].mean()

print(f"Total Sales: ${total_sales:.2f}")
print(f"Total Transactions: {total_transactions}")
print(f"Total Customers: {total_customers}")
print(f"Average Transaction Value: ${average_transaction:.2f}")

# ==========================================================
# SALES BY LIFESTAGE
# ==========================================================

sales_lifestage = (
    merged_data
    .groupby("LIFESTAGE")["TOT_SALES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Lifestage")
print(sales_lifestage)

# ==========================================================
# SALES BY PREMIUM CUSTOMER
# ==========================================================

sales_premium = (
    merged_data
    .groupby("PREMIUM_CUSTOMER")["TOT_SALES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Premium Customer")
print(sales_premium)

# ==========================================================
# TOP 10 BRANDS
# ==========================================================

top_brands = (
    merged_data
    .groupby("BRAND")["TOT_SALES"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Brands")
print(top_brands)

# ==========================================================
# TOP 10 PACK SIZES
# ==========================================================

top_pack = (
    merged_data
    .groupby("PACK_SIZE")["TOT_SALES"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop Pack Sizes")
print(top_pack)

# ==========================================================
# MOST FREQUENT CUSTOMERS
# ==========================================================

top_customers = (
    merged_data
    .groupby("LYLTY_CARD_NBR")
    .agg(
        Total_Sales=("TOT_SALES","sum"),
        Transactions=("TXN_ID","count")
    )
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

print("\nTop Customers")
print(top_customers)

# ==========================================================
# VISUALIZATIONS
# ==========================================================

print("\n" + "="*60)
print("CREATING VISUALIZATIONS")
print("="*60)

# Set chart style
plt.style.use("ggplot")

# ----------------------------------------------------------
# Sales by Lifestage
# ----------------------------------------------------------

plt.figure(figsize=(10,6))

sales_lifestage.sort_values().plot(kind="barh")

plt.title("Total Sales by Customer Lifestage")
plt.xlabel("Total Sales ($)")
plt.ylabel("Lifestage")

plt.tight_layout()
plt.savefig("Sales_by_Lifestage.png")
plt.show()

# ----------------------------------------------------------
# Sales by Premium Customer
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

sales_premium.plot(kind="bar")

plt.title("Sales by Premium Customer Type")
plt.xlabel("Customer Type")
plt.ylabel("Total Sales ($)")

plt.tight_layout()
plt.savefig("Sales_by_Premium_Customer.png")
plt.show()

# ----------------------------------------------------------
# Top 10 Brands
# ----------------------------------------------------------

plt.figure(figsize=(12,6))

top_brands.sort_values().plot(kind="barh")

plt.title("Top 10 Chip Brands")
plt.xlabel("Sales ($)")
plt.ylabel("Brand")

plt.tight_layout()
plt.savefig("Top_10_Brands.png")
plt.show()

# ----------------------------------------------------------
# Top Pack Sizes
# ----------------------------------------------------------

plt.figure(figsize=(10,6))

top_pack.sort_values().plot(kind="bar")

plt.title("Top Pack Sizes")
plt.xlabel("Pack Size (g)")
plt.ylabel("Sales ($)")

plt.tight_layout()
plt.savefig("Top_Pack_Sizes.png")
plt.show()

# ==========================================================
# SAVE CLEANED DATA
# ==========================================================

transaction_data.to_csv(
    "Cleaned_Transaction_Data.csv",
    index=False
)

purchase_behaviour.to_csv(
    "Cleaned_Purchase_Behaviour.csv",
    index=False
)

merged_data.to_csv(
    "Merged_Customer_Transaction_Data.csv",
    index=False
)

print("\nCleaned datasets saved successfully.")

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

print("\n" + "="*60)
print("BUSINESS INSIGHTS")
print("="*60)

print(f"""
1. Total Revenue Generated : ${total_sales:.2f}

2. Total Customers : {total_customers}

3. Total Transactions : {total_transactions}

4. Average Transaction Value : ${average_transaction:.2f}

5. Highest Revenue Customer Segment:
{sales_lifestage.idxmax()}

6. Highest Revenue Customer Type:
{sales_premium.idxmax()}

7. Best Selling Brand:
{top_brands.idxmax()}

8. Most Popular Pack Size:
{top_pack.idxmax()} g
""")

# ==========================================================
# COMMERCIAL RECOMMENDATIONS
# ==========================================================

print("\n" + "="*60)
print("COMMERCIAL RECOMMENDATIONS")
print("="*60)

print("""
Recommendation 1:
Focus marketing campaigns on the highest revenue customer segment.

Recommendation 2:
Increase shelf space for the highest selling chip brand.

Recommendation 3:
Maintain sufficient inventory for the most popular pack size.

Recommendation 4:
Develop loyalty offers for Premium customers to increase repeat purchases.

Recommendation 5:
Introduce targeted promotions for lower performing customer segments.

Recommendation 6:
Use customer purchasing behaviour to personalize future promotions.
""")

# ==========================================================
# END OF PROJECT
# ==========================================================

print("\n" + "="*60)
print("TASK 1 COMPLETED SUCCESSFULLY")
print("="*60)