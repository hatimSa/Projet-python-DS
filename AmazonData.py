import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Configuration du navigateur Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode sans tête pour exécuter sans interface graphique

# Créer une instance du navigateur
driver = webdriver.Chrome(options=options)

# URL de recherche initiale sur Amazon
amazon_url = "https://www.amazon.com/s?k=gaming&ref=nb_sb_noss"

# Préparer le fichier CSV
with open("amazon_products_gaming.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating", "Link", "Description"])  # En-têtes des colonnes

    # Naviguer vers la page Amazon
    driver.get(amazon_url)
    driver.implicitly_wait(10)  # Attendre que la page soit complètement chargée

    # Boucle pour extraire les produits
    page_number = 1
    extracted_links = set()  # Pour éviter les doublons
    while True:
        print(f"Scraping page {page_number}...")

        # Obtenir le contenu HTML de la page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extraire les produits
        products = soup.find_all("div", class_="sg-col-inner")
        if not products:
            print("No more products found. Stopping extraction.")
            break

        for product in products:
            try:
                # Titre
                title_element = product.find("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
                title = title_element.text.strip() if title_element else "Title not found"

                # Prix
                price_element = product.find("span", class_="a-offscreen")
                price = price_element.text.strip() if price_element else "Price not found"

                # Évaluation
                rating_element = product.find("span", class_="a-icon-alt")
                rating = rating_element.text.strip() if rating_element else "Rating not found"

                # Lien du produit
                link_element = product.find("a", class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal")
                product_link = "https://www.amazon.com" + link_element.attrs["href"] if link_element else "Link not found"

                # Vérifier si le lien a déjà été extrait
                if product_link not in extracted_links and product_link != "Link not found":
                    extracted_links.add(product_link)

                    # Accéder à la page du produit pour extraire la description
                    driver.get(product_link)
                    driver.implicitly_wait(10)  # Attendre que la page du produit se charge
                    product_soup = BeautifulSoup(driver.page_source, "html.parser")

                    description_element = product_soup.find("div", id="feature-bullets")
                    description = (
                        description_element.text.strip().replace("\n", " ")
                        if description_element
                        else "Description not found"
                    )

                    # Écrire les données dans le fichier CSV
                    writer.writerow([title, price, rating, product_link, description])

                    # Afficher les données dans le terminal
                    print(f"Title: {title}")
                    print(f"Price: {price}")
                    print(f"Rating: {rating}")
                    print(f"Link: {product_link}")
                    print(f"Description: {description}")
                    print("-" * 50)
                else:
                    print("Duplicate product link, skipping.")

            except Exception as e:
                print(f"Error extracting product: {e}")

        # Vérifier si un bouton "Suivant" existe pour continuer
        next_page = soup.find("li", class_="a-last")
        if next_page and next_page.find("a"):
            next_page_link = "https://www.amazon.com" + next_page.find("a")["href"]
            driver.get(next_page_link)
            page_number += 1
            time.sleep(2)  # Pause pour éviter les requêtes excessives
        else:
            print("No more pages. Stopping extraction.")
            break

# Quitter le navigateur
driver.quit()
print("Extraction terminée, données enregistrées dans 'amazon_products_gaming.csv'.")
