import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données nettoyées
file_path = "ebay_products_pc_gamer_cleaned.csv"
df = pd.read_csv(file_path)

# Appliquer un style Seaborn
sns.set(style="whitegrid")

# 1. **Histogramme : Distribution des prix**
plt.figure(figsize=(10, 6))
sns.histplot(df["Price"], bins=30, kde=True, color="blue")
plt.xlabel("Prix (USD)")
plt.ylabel("Nombre de produits")
plt.title("Distribution des prix des PC Gamer sur eBay")
plt.show()

# 2. **Top 10 Produits les Plus Chers**
top_10_expensive = df.nlargest(10, "Price")
plt.figure(figsize=(12, 6))
sns.barplot(y=top_10_expensive["Title"], x=top_10_expensive["Price"], palette="coolwarm")
plt.xlabel("Prix (USD)")
plt.ylabel("Titre du produit")
plt.title("Top 10 des PC Gamer les plus chers sur eBay")
plt.show()

# 3. **Nombre de produits par pays**
plt.figure(figsize=(10, 6))
country_counts = df["Country"].value_counts()
sns.barplot(x=country_counts.index, y=country_counts.values, palette="mako")
plt.xlabel("Pays")
plt.ylabel("Nombre de produits")
plt.title("Nombre de PC Gamer par pays sur eBay")
plt.xticks(rotation=45)
plt.show()

# 4. **Répartition des Promotions**
plt.figure(figsize=(8, 8))
promotion_counts = df["Promotion"].value_counts()
plt.pie(promotion_counts, labels=promotion_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
plt.title("Répartition des promotions sur eBay")
plt.show()
