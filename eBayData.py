import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/b/Video-Games-Consoles/1249/bn_1850232"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("section", class_="brw-product-carousel brw-limited-time-deals bltd")

    print(f"{len(products)} produits trouvés!!!")

    for product in products:
        try:
            title = product.find("h3", class_="textual-display bsig__title__text")
            old_price = product.find("span", class_="textual-display bsig__price bsig__price--displayprice")
            price_promo = product.find("span", class_="textual-display bsig__generic bsig__previousPrice strikethrough")
            link = product.find("a", class_="brw-product-card__image-link")

            print(f"Titre: {title.text.strip() if title else 'N/A'}")
            print(f"Prix normal: {old_price.text.strip() if old_price else 'N/A'}")
            print(f"Prix promo: {price_promo.text.strip() if price_promo else 'N/A'}")
            print(f"Link: {link}")
            print("-" * 50)

        except Exception as e:
            print(f"Error extracting product: {e}")
else:
    print(f"Erreur lors de la récupération de la page principale. Code : {response.status_code}")