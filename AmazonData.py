from selenium import webdriver
from bs4 import BeautifulSoup

# Configuration du navigateur Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Créer une instance du navigateur
driver = webdriver.Chrome(options=options)

amazon_url = "https://www.amazon.com/s?k=gaming&ref=nb_sb_noss"
driver.get(amazon_url)

# Attendre que la page soit complètement chargée (par exemple, attendre un élément spécifique)
driver.implicitly_wait(10)

# Obtenir le contenu HTML de la page
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extraction des produits
products = soup.find_all("div", class_="sg-col-inner")

# Set pour suivre les liens déjà extraits
extracted_links = set()

for product in products:
    try:
        title_element = product.find("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Product title not found"

        price_element = product.find("span", class_="a-offscreen")
        if price_element:
            price = price_element.text.strip()
        else:
            price = "Price not found"

        rating_element = product.find("span", class_="a-icon-alt")
        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = "Rating not found"

        link_element = product.find("a", class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal")
        if link_element:
            product_link = "https://www.amazon.com" + link_element.attrs["href"]
        else:
            product_link = "Product link not found"

        # Vérifier si le lien du produit a déjà été extrait
        if product_link not in extracted_links:
            extracted_links.add(product_link)
            print(f"Product Title: {title}")
            print(f"Price: {price}")
            print(f"Rating: {rating}")
            print(f"Product Link: {product_link}")
            
            # Accéder à la page du produit pour extraire la description
            driver.get(product_link)
            driver.implicitly_wait(10)  # Attendre que la page du produit se charge
            
            # Extraire la description du produit
            product_soup = BeautifulSoup(driver.page_source, "html.parser")
            description_element = product_soup.find("div", id="feature-bullets")

            if description_element:
                description = description_element.text.strip()
                print(f"Description: {description}")
            else:
                print("Description not found")
            
            print("-" * 50)
        else:
            print("Duplicate product, skipping.")

    except Exception as e:
        print(f"Error extracting product: {e}")

driver.quit()