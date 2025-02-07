import pandas as pd
import re

# Load the CSV file
df = pd.read_csv("jumia_products.csv")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Replace "N/A" with NaN and remove missing values
df.replace("N/A", pd.NA, inplace=True)
df.dropna(inplace=True)

# Function to clean price values
def clean_price(price):
    if pd.isna(price):
        return None
    # Extract only the first valid price (to handle cases like '490.00590.00')
    match = re.search(r"\d+(\.\d+)?", str(price))
    return float(match.group()) if match else None

# Apply cleaning to price columns
df["Old Price"] = df["Old Price"].apply(clean_price)
df["Promotional Price"] = df["Promotional Price"].apply(clean_price)

# Function to clean rating values
def clean_rating(rating):
    match = re.search(r"\d+(\.\d+)?", str(rating))
    return float(match.group()) if match else None

df["Rating"] = df["Rating"].apply(clean_rating)

# Save the cleaned data
df.to_csv("jumia_products_cleaned.csv", index=False, encoding="utf-8")

print("Data cleaning complete. Saved as 'jumia_products_cleaned.csv'.")