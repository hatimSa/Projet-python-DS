import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Charger les fichiers CSV
amazon_df = pd.read_csv("amazon_products_gaming.csv")
ebay_df = pd.read_csv("ebay_products_pc_gamer.csv")

# Fonction pour nettoyer les prix et convertir en float
def clean_price(price):
    if isinstance(price, str):
        # Supprime les caractères non numériques sauf le point
        price = re.sub(r'[^\d.]', '', price)
        
        # Si plusieurs points décimaux, garder uniquement le premier
        if price.count('.') > 1:
            price = price.split('.')[0] + '.' + ''.join(price.split('.')[1:])
        
        try:
            return float(price) if price else None
        except ValueError:
            return None
    return None

# Nettoyage des prix
amazon_df["Price"] = amazon_df["Price"].apply(clean_price)
ebay_df["Price"] = ebay_df["Price"].apply(clean_price)

# Supprimer les lignes avec prix manquants
amazon_df = amazon_df.dropna(subset=["Price"])
ebay_df = ebay_df.dropna(subset=["Price"])

# Associer les produits par mots-clés communs (exemple simplifié avec la présence de "gaming")
amazon_df["Category"] = amazon_df["Title"].apply(lambda x: "Gaming" if "gaming" in str(x).lower() else "Other")
ebay_df["Category"] = ebay_df["Title"].apply(lambda x: "Gaming" if "gaming" in str(x).lower() else "Other")

# Renommer les colonnes pour éviter les confusions
amazon_df.rename(columns={"Price": "Prix_Amazon"}, inplace=True)
ebay_df.rename(columns={"Price": "Prix_eBay"}, inplace=True)

# Fusionner les jeux par titre proche (simplifié ici en prenant une partie du nom)
merged_df = pd.merge(amazon_df, ebay_df, on="Category", suffixes=("_Amazon", "_eBay"))

# Tracer un scatter plot pour comparer les prix
plt.figure(figsize=(10, 6))
sns.scatterplot(x=merged_df["Prix_Amazon"], y=merged_df["Prix_eBay"], hue=merged_df["Category"], alpha=0.7, edgecolor="k")
plt.xlabel("Prix Amazon ($)")
plt.ylabel("Prix eBay ($)")
plt.title("Comparaison des prix Amazon vs eBay")
plt.legend(title="Catégorie")
plt.grid(True)
plt.show()

# Tracer un boxplot pour comparer les distributions de prix
plt.figure(figsize=(10, 6))
merged_df_melted = pd.melt(merged_df, id_vars=["Category"], value_vars=["Prix_Amazon", "Prix_eBay"], var_name="Site", value_name="Prix")
sns.boxplot(x="Site", y="Prix", hue="Category", data=merged_df_melted)
plt.title("Distribution des prix sur Amazon et eBay")
plt.xlabel("Site de vente")
plt.ylabel("Prix ($)")
plt.legend(title="Catégorie")
plt.grid(True)
plt.show()
