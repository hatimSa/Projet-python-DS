import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données nettoyées
df = pd.read_csv("jumia_products_cleaned.csv")

# Définir le style de visualisation
sns.set_style("whitegrid")

# Créer une figure avec plusieurs sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1️⃣ Histogramme des prix promotionnels
sns.histplot(df["Promotional Price"], bins=30, kde=True, color="green", ax=axes[0, 0])
axes[0, 0].set_title("Distribution des Prix Promotionnels")
axes[0, 0].set_xlabel("Prix (MAD)")

# 2️⃣ Boxplot des prix avant et après promo
df_melted = df.melt(value_vars=["Old Price", "Promotional Price"], var_name="Type de Prix", value_name="Prix")
sns.boxplot(x="Type de Prix", y="Prix", data=df_melted, palette=["red", "green"], ax=axes[0, 1])
axes[0, 1].set_title("Comparaison des Prix Avant/Après Promo")

# 3️⃣ Courbe des prix (triée pour voir l'évolution)
df_sorted = df.sort_values(by="Promotional Price")
axes[1, 0].plot(df_sorted["Promotional Price"].values, label="Prix Promo", color="green", marker="o", linestyle="-")
axes[1, 0].plot(df_sorted["Old Price"].values, label="Prix Normal", color="red", marker="x", linestyle="--")
axes[1, 0].set_title("Comparaison des Prix Avant/Après Promo")
axes[1, 0].set_ylabel("Prix (MAD)")
axes[1, 0].legend()

# 4️⃣ Distribution des notes (ratings)
sns.histplot(df["Rating"].dropna(), bins=10, kde=True, color="blue", ax=axes[1, 1])
axes[1, 1].set_title("Distribution des Notes des Produits")
axes[1, 1].set_xlabel("Note")

# Ajuster l'espacement
plt.tight_layout()
plt.show()