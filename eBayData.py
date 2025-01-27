import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration du navigateur Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode sans tête pour exécuter sans interface graphique
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

# Créer une instance du navigateur
driver = webdriver.Chrome(options=options)

# URL de recherche initiale sur eBay
ebay_url = "https://www.ebay.com/sch/i.html?_nkw=pc+gamer&_sacat=0&_from=R40&_trksid=p4432023.m570.l1311"

# Préparer le fichier CSV
with open("ebay_products_pc_gamer.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating", "Link", "Description", "Promotion"])

    page_number = 1  # Débuter à la première page
    while True:
        # Construire l'URL pour la page courante
        url = f"{ebay_url}&_pgn={page_number}"
        driver.get(url)

        # Attendre que les éléments produits apparaissent
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
            )
        except Exception as e:
            print(f"Erreur lors du chargement de la page {page_number}: {e}")
            break

        # Récupérer le contenu de la page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extraire les éléments produits
        products = soup.find_all("li", class_="s-item")
        if not products:  # Si aucun produit n'est trouvé, arrêter la boucle
            print(f"Aucun produit trouvé sur la page {page_number}. Fin de l'extraction.")
            break

        for product in products:
            try:
                # Titre
                title_element = product.find("div", class_="s-item__title")
                title = title_element.text.strip() if title_element else "Titre non trouvé"

                # Prix
                price_element = product.find("span", class_="s-item__price")
                price = price_element.text.strip() if price_element else "Prix non trouvé"

                # Lien
                link_element = product.find("a", class_="s-item__link")
                product_link = link_element["href"] if link_element else "Lien non trouvé"

                # Visiter la page du produit pour extraire Rating, Description et Promotion
                if product_link != "Lien non trouvé":
                    driver.get(product_link)
                    driver.implicitly_wait(10)
                    product_soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Note du produit
                    rating_element = product_soup.find("div", class_="reviews-seeAll-hdn")
                    rating = rating_element.text.strip() if rating_element else "Note non trouvée"

                    # Description
                    description_element = product_soup.find("div", id="viTabs_0_is")
                    description = description_element.text.strip() if description_element else "Description non trouvée"

                    # Promotion (extraire depuis la page produit)
                    promotion_element = product_soup.find("span", class_="ux-textspans ux-textspans--EMPHASIS")
                    promotion = promotion_element.text.strip() if promotion_element else "Pas de promotion"
                else:
                    rating = "Note non trouvée"
                    description = "Description non trouvée"
                    promotion = "Pas de promotion"

                # Écrire les données dans le fichier CSV
                writer.writerow([title, price, rating, product_link, description, promotion])

                # Afficher les données
                print(f"Product Title: {title}")
                print(f"Price: {price}")
                print(f"Rating: {rating}")
                print(f"Product Link: {product_link}")
                print(f"Description: {description}")
                print(f"Promotion: {promotion}")
                print("-" * 50)

            except Exception as e:
                print(f"Erreur lors de l'extraction d'un produit : {e}")

        # Passer à la page suivante
        page_number += 1
        time.sleep(2)  # Pause pour éviter d'envoyer trop de requêtes

# Quitter le navigateur
driver.quit()
print("Extraction terminée, données enregistrées dans 'ebay_products.csv'.")