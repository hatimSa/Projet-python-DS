from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configuration de Selenium
options = Options()
options.add_argument("--headless")  # Mode sans interface graphique
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# Lancer le navigateur
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

try:
    url = "https://www.ebay.com/b/Video-Games-Consoles/1249/bn_1850232"
    print("Navigating to eBay...")
    driver.get(url)

    # Attendre que la page se charge complètement
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "carousel__viewport"))
    )

    # Obtenir le contenu HTML de la page principale
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("a", class_="bsig__title__wrapper")

    print(f"{len(products)} produits trouvés.")

    for product in products[:5]:  # Limiter à 5 produits pour le test
        try:
            title = product.find("h3", class_="textual-display bsig__title__text")
            price_new = product.find("span", class_="textual-display bsig__price bsig__price--newprice")
            price_used = product.find("span", class_="textual-display bsig__price bsig__price--usedprice")
            rating = product.find("div", class_="star-rating")
            link = product.find("a", class_="bsig__title__wrapper")

            product_link = product['href']

            print(f"Titre: {title.text.strip() if title else 'N/A'}")
            print(f"Prix normal: {price_new.text.strip() if price_new else 'N/A'}")
            print(f"Prix utilisé: {price_used.text.strip() if price_used else 'N/A'}")
            print(f"Note: {rating.text.strip() if rating else 'N/A'}")
            print(f"Link: {product_link}")

            # Vérifier si le lien est déjà complet
            if not product_link.startswith("https://"):
                product_link = f"https://www.ebay.com{product_link}"

            print(f"Accès au produit : {product_link}")
            
            # Naviguer vers la page du produit
            driver.get(product_link)
            time.sleep(3)  # Attendre que la page du produit se charge

            # Extraire la description
            product_soup = BeautifulSoup(driver.page_source, "html.parser")
            description = product_soup.find("section", class_="product-spectification").text.strip() if product_soup.find("section", class_="product-spectification") else "Description non trouvée"
            
            print(f"Description : {description}")
            print("-" * 50)

        except Exception as e:
            print(f"Erreur lors de l'accès au produit : {e}")

finally:
    driver.quit()