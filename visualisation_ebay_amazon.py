import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les fichiers nettoyés
amazon_file = "amazon_products_gaming_cleaned.csv"
ebay_file = "ebay_products_pc_gamer_cleaned.csv"

df_amazon = pd.read_csv(amazon_file)
df_ebay = pd.read_csv(ebay_file)

# Ajouter une colonne Source
df_amazon["Source"] = "Amazon"
df_ebay["Source"] = "eBay"

# Vérifier si une colonne "Category" existe, sinon ajouter une (ex: baser sur le titre)
df_amazon["Category"] = df_amazon["Title"].apply(lambda x: "Gaming" if "gaming" in x.lower() else "Other")
df_ebay["Category"] = df_ebay["Title"].apply(lambda x: "PC Gamer" if "pc" in x.lower() or "gamer" in x.lower() else "Other")

# Fusionner les datasets
df_combined = pd.concat([df_amazon, df_ebay], ignore_index=True)

# Convertir les prix en numérique
df_combined["Price"] = pd.to_numeric(df_combined["Price"], errors="coerce")

# Filtrer les valeurs valides
df_combined = df_combined.dropna(subset=["Price", "Category"])

# Appliquer le style Seaborn
sns.set(style="whitegrid")

# 1️⃣ **Histogramme de distribution des prix par catégorie**
plt.figure(figsize=(12, 6))
sns.histplot(data=df_combined, x="Price", hue="Category", bins=30, kde=True, palette="viridis")
plt.xlabel("Prix (USD)")
plt.ylabel("Nombre de produits")
plt.title("Distribution des prix par catégorie")
plt.legend(title="Catégorie")
plt.show()

# 2️⃣ **Boxplot pour comparer les prix par catégorie**
plt.figure(figsize=(12, 6))
sns.boxplot(x="Category", y="Price", data=df_combined, hue="Source", palette=["blue", "red"])
plt.xlabel("Catégorie")
plt.ylabel("Prix (USD)")
plt.title("Comparaison des prix par catégorie entre Amazon et eBay")
plt.show()

# 3️⃣ **Distribution KDE des prix par catégorie**
plt.figure(figsize=(12, 6))
sns.kdeplot(data=df_combined, x="Price", hue="Category", fill=True, palette="magma")
plt.xlabel("Prix (USD)")
plt.ylabel("Densité")
plt.title("Densité des prix par catégorie")
plt.show()
