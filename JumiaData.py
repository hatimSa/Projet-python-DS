import csv
import requests
from bs4 import BeautifulSoup

# URL de la page Jumia
url = "https://www.jumia.ma/jeux-videos-consoles/"

# Préparer le fichier CSV
with open("jumia_products.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # En-têtes des colonnes
    writer.writerow(["Title", "Old Price", "Promotional Price", "Rating", "Link", "Description"])

    # Récupérer le contenu de la page principale
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraire les produits
        products = soup.find_all("article", class_="prd _fb col c-prd")
        print(f"{len(products)} produits trouvés!!!")

        for product in products:
            try:
                # Titre
                title_element = product.find("h3", class_="name")
                title = title_element.text.strip() if title_element else "N/A"

                # Prix normal
                old_price_element = product.find("div", class_="old")
                old_price = old_price_element.text.strip() if old_price_element else "N/A"

                # Prix promotionnel
                promo_price_element = product.find("div", class_="prc")
                promo_price = promo_price_element.text.strip() if promo_price_element else "N/A"

                # Note
                rating_element = product.find("div", class_="stars _s")
                rating = rating_element.text.strip() if rating_element else "N/A"

                # Lien du produit
                link_element = product.find("a", class_="core")
                product_link = f"https://www.jumia.ma{link_element['href']}" if link_element else "N/A"

                # Description
                description = "N/A"
                if product_link and product_link != "N/A":
                    product_response = requests.get(product_link)
                    if product_response.status_code == 200:
                        product_soup = BeautifulSoup(product_response.text, "html.parser")
                        description_element = product_soup.find("div", class_="markup -mhm -pvl -oxa -sc")
                        description = description_element.text.strip() if description_element else "N/A"

                # Écrire les données dans le fichier CSV
                writer.writerow([title, old_price, promo_price, rating, product_link, description])

                # Afficher les données dans le terminal
                print(f"Titre: {title}")
                print(f"Prix normal: {old_price}")
                print(f"Prix promo: {promo_price}")
                print(f"Note: {rating}")
                print(f"Link: {product_link}")
                print(f"Description: {description}")
                print("-" * 50)

            except Exception as e:
                print(f"Erreur lors de l'extraction d'un produit : {e}")

    else:
        print(f"Erreur lors de la récupération de la page principale. Code : {response.status_code}")

print("Extraction terminée, données enregistrées dans 'jumia_products.csv'.")
