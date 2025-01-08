import requests
from bs4 import BeautifulSoup

url = "https://www.jumia.ma/jeux-videos-consoles/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("article", class_="prd _fb col c-prd")

    print(f"{len(products)} produits trouvés!!!")

    for product in products:
        try:
            title = product.find("h3", class_="name")
            old_price = product.find("div", class_="old")
            price_promo = product.find("div", class_="prc")
            rating = product.find("div", class_="stars _s")
            link = product.find("a", class_="core")

            # Construire le lien complet du produit
            product_link = f"https://www.jumia.ma{link['href']}" if link else None

            print(f"Titre: {title.text.strip() if title else 'N/A'}")
            print(f"Prix normal: {old_price.text.strip() if old_price else 'N/A'}")
            print(f"Prix promo: {price_promo.text.strip() if price_promo else 'N/A'}")
            print(f"Note: {rating.text.strip() if rating else 'N/A'}")
            print(f"Link: {product_link}")

            # Accéder à la page du produit pour extraire la description
            if product_link:
                product_response = requests.get(product_link)
                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, "html.parser")

                    description = product_soup.find("div", class_="markup -mhm -pvl -oxa -sc")

                    print(f"Description: {description.text.strip() if description else 'N/A'}")
                else:
                    print("Erreur lors de l'accès à la page du produit.")
            print("-" * 50)

        except Exception as e:
            print(f"Error extracting product: {e}")
else:
    print(f"Erreur lors de la récupération de la page principale. Code : {response.status_code}")