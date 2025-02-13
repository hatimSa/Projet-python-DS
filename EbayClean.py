import pandas as pd

# Charger les données
file_path = "ebay_products_pc_gamer.csv"
df = pd.read_csv(file_path, dtype=str).dropna()

# Supprimer les espaces inutiles dans toutes les colonnes
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Correction des prix : garder uniquement la première valeur numérique correcte
def clean_price(price):
    if not isinstance(price, str) or "Prix non trouvé" in price:
        return None

    # Extraire uniquement les chiffres et points
    cleaned_prices = ''.join(c if c.isdigit() or c == '.' else ' ' for c in price).split()

    # Prendre le premier prix valide
    if cleaned_prices:
        try:
            return float(cleaned_prices[0])  # Convertir en float
        except ValueError:
            return None  # Ignorer les erreurs de conversion

    return None

df["Price"] = df["Price"].apply(clean_price)

# Suppression des doublons basés sur le lien
df.drop_duplicates(subset="Link", keep="first", inplace=True)

# Nettoyage des descriptions et promotions (supprime les espaces inutiles)
df["Description"] = df["Description"].str.replace(r"\s+", " ", regex=True)
df["Promotion"] = df["Promotion"].str.replace(r"\s+", " ", regex=True)

# Supprimer les lignes où le prix est manquant ou invalide
df.dropna(subset=["Title", "Price"], inplace=True)

# Enregistrement du fichier nettoyé
clean_file_path = "ebay_products_pc_gamer_cleaned.csv"
df.to_csv(clean_file_path, index=False, encoding="utf-8")

print(f"Nettoyage terminé ! Données sauvegardées dans '{clean_file_path}'.")