import pandas as pd

# Charger les données
file_path = "amazon_products_gaming.csv"

# Lire le fichier CSV en ignorant les lignes vides
df = pd.read_csv(file_path, dtype=str).dropna()

# Supprimer les espaces inutiles dans toutes les colonnes
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Correction des prix (ex: "490.00590.00" → "490.00")
def clean_price(price):
    if "Price not found" in price:
        return None
    clean_p = ''.join(c if c.isdigit() or c == '.' else '' for c in price)
    parts = clean_p.split('.')
    if len(parts) > 2:
        clean_p = f"{parts[0]}.{parts[1]}"  # Garder uniquement la première partie correcte
    return float(clean_p) if clean_p else None

df["Price"] = df["Price"].apply(clean_price)

# Conversion des évaluations en numérique
def clean_rating(rating):
    if "Rating not found" in rating:
        return None
    try:
        return float(rating.split()[0])  # Garde uniquement le chiffre avant "out of 5 stars"
    except:
        return None

df["Rating"] = df["Rating"].apply(clean_rating)

# Suppression des doublons basés sur le lien
df.drop_duplicates(subset="Link", keep="first", inplace=True)

# Nettoyage des descriptions (supprime les espaces et les caractères spéciaux inutiles)
df["Description"] = df["Description"].str.replace(r"\s+", " ", regex=True)

# Suppression des lignes où le prix ou le titre est manquant
df.dropna(subset=["Title", "Price"], inplace=True)

# Enregistrement du fichier nettoyé
clean_file_path = "amazon_products_gaming_cleaned.csv"
df.to_csv(clean_file_path, index=False, encoding="utf-8")

print(f"Nettoyage terminé ! Données sauvegardées dans '{clean_file_path}'.")