import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
file_path = "amazon_products_gaming_cleaned.csv"
df = pd.read_csv(file_path)

# Set Seaborn style for better visuals
sns.set(style="whitegrid")

# 1. **Histogram: Price Distribution**
plt.figure(figsize=(10, 6))
sns.histplot(df["Price"], bins=30, kde=True, color="blue")
plt.xlabel("Price (USD)")
plt.ylabel("Count")
plt.title("Price Distribution of Amazon Gaming Products")
plt.show()

# 2. **Bar Chart: Average Price per Rating**
df_grouped = df.groupby("Rating")["Price"].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x="Rating", y="Price", data=df_grouped, palette="viridis")
plt.xlabel("Rating")
plt.ylabel("Average Price (USD)")
plt.title("Average Price by Rating on Amazon")
plt.xticks(rotation=45)
plt.show()

# 3. **Scatter Plot: Price vs. Rating**
plt.figure(figsize=(10, 6))
sns.scatterplot(x="Rating", y="Price", data=df, alpha=0.6, color="red")
plt.xlabel("Rating")
plt.ylabel("Price (USD)")
plt.title("Price vs. Rating for Amazon Gaming Products")
plt.show()

# 4. **Top 10 Most Expensive Products**
top_10_expensive = df.nlargest(10, "Price")
plt.figure(figsize=(12, 6))
sns.barplot(y=top_10_expensive["Title"], x=top_10_expensive["Price"], palette="coolwarm")
plt.xlabel("Price (USD)")
plt.ylabel("Product Title")
plt.title("Top 10 Most Expensive Gaming Products on Amazon")
plt.show()
