import os
import csv
import requests
import time
from bs4 import BeautifulSoup

# URL de la première page Jumia
base_url = "https://www.jumia.ma/jeux-videos-consoles/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Vérifier si le fichier CSV existe déjà
file_exists = os.path.isfile("jumia_products.csv")

# Ouvrir le fichier CSV en mode ajout ("a")
with open("jumia_products.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Écrire les en-têtes si le fichier n'existe pas encore
    if not file_exists:
        writer.writerow(["Title", "Old Price", "Promotional Price", "Rating", "Link", "Description"])

    page_number = 1
    while True:
        # Construire l'URL de la page courante
        url = f"{base_url}?page={page_number}"
        print(f"Scraping page {page_number}...")

        # Récupérer le contenu de la page
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de la page {page_number}. Code : {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Extraire les produits
        products = soup.find_all("article", class_="prd _fb col c-prd")
        if not products:  # Si aucun produit n'est trouvé, arrêter la boucle
            print(f"Aucun produit trouvé sur la page {page_number}. Fin de l'extraction.")
            break

        print(f"{len(products)} produits trouvés sur la page {page_number}.")

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

                # Note (rating)
                rating_element = product.find("div", class_="stars _s")
                rating = rating_element.text.strip() if rating_element else "Pas de note"

                # Lien du produit
                link_element = product.find("a", class_="core")
                product_link = f"https://www.jumia.ma{link_element['href']}" if link_element else "N/A"

                # Description (extraite depuis la page produit)
                description = "N/A"
                if product_link != "N/A":
                    product_response = requests.get(product_link, headers=headers)
                    if product_response.status_code == 200:
                        product_soup = BeautifulSoup(product_response.text, "html.parser")
                        description_element = product_soup.find("div", class_="markup -mhm -pvl -oxa -sc")
                        description = description_element.text.strip() if description_element else "N/A"
                    else:
                        print(f"Erreur en visitant le produit : {product_link}")

                # Écrire les données dans le fichier CSV
                writer.writerow([title, old_price, promo_price, rating, product_link, description])

                # Afficher les données
                print(f"Titre: {title}")
                print(f"Prix normal: {old_price}")
                print(f"Prix promo: {promo_price}")
                print(f"Note: {rating}")
                print(f"Link: {product_link}")
                print(f"Description: {description}")
                print("-" * 50)

            except Exception as e:
                print(f"Erreur lors de l'extraction d'un produit : {e}")

        # Passer à la page suivante
        page_number += 1
        time.sleep(2)  # Pause pour éviter d'être bloqué

print("Extraction terminée, données enregistrées dans 'jumia_products.csv'.")