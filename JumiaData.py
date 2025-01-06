from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurer les options de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Commentez cette ligne si vous voulez voir le navigateur

# Chemin vers votre chromedriver
service = Service("C:/Users/Hatim/Downloads/chromedriver-win64/chromedriver.exe")  # Remplacez par le chemin vers votre chromedriver

# Lancer le navigateur avec les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accéder à la page Jumia
url = "https://www.jumia.ma/jeux-videos-consoles/"
driver.get(url)

# Faire défiler la page vers le bas pour charger les produits
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # Attendez un peu que les produits se chargent

# Afficher le HTML de la page pour déboguer
print(driver.page_source)

# Attente explicite pour que les éléments de produits soient présents
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title-class")))

# Extraire les produits
products = driver.find_elements(By.CSS_SELECTOR, ".title-class")
print(f"Found {len(products)} products.")

# Limiter le nombre de produits à 5
max_products = 5
product_count = 0

# Parcourir chaque produit trouvé
for product in products:
    if product_count >= max_products:
        break  # Sortir de la boucle si 5 produits ont été extraits
    
    try:
        title = product.find_element(By.CSS_SELECTOR, ".name")
        price = product.find_element(By.CSS_SELECTOR, ".price")
        
        print(f"Title: {title.text.strip() if title else 'N/A'}")
        print(f"Price: {price.text.strip() if price else 'N/A'}")
        print("-" * 50)
        
        product_count += 1  # Incrémenter le compteur après chaque produit extrait

    except Exception as e:
        print(f"Error extracting product: {e}")

# Fermer le navigateur
driver.quit()