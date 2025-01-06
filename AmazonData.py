import requests
from bs4 import BeautifulSoup

amazon_url = "https://www.amazon.com/RedThunder-Wireless-Rechargeable-Mechanical-Anti-ghosting/dp/B09BR46F63/ref=sr_1_1_sspa?_encoding=UTF8&content-id=amzn1.sym.3ee8a8b8-12a8-4ba9-9886-109b6d3579a2&dib=eyJ2IjoiMSJ9.QjBFM_c24i1J6qA0sqOIwIIWX3m9tFhYPU-D3vb-8EcI7EljpVOYCRmjEi2pg6QYEMyZ8DwhgMnZSP97rUv8Ezfe8IyQhcDZMCGe118TvBVkCfnUMOqyyQk-EUmA_MY5cW-FdUZnq1bbVsF9qSjIht2FkGERjn7VAtXrr5zKqr1PrDUq-tgaO4w5gnZze3wn8ZnstFO1eJDKTQA82d2i-oAbk1Z2vi58Ich0cykj465ShSKaPz80r0QmyFGpJaUHz2fp-OPUeGo1JPnktMbsDEGoUbRUma1lkZ0UOZv0iPo.y6BeWZwY44ODHRmOei0h4gKy7k75OrF5AI6P1ckmA98&dib_tag=se&keywords=gaming&pd_rd_r=07e18d56-767a-45da-8a41-ed1086364614&pd_rd_w=JqqCY&pd_rd_wg=v6442&pf_rd_p=3ee8a8b8-12a8-4ba9-9886-109b6d3579a2&pf_rd_r=27RHMP5RYYGG0QV0KMRD&qid=1736187946&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

amazon_custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

amazon_cookies = {
    'session-id': '131-1289666-6087523',
    'ubid-main': '131-9196836-4366522',
    'x-main': '"MycvhchDeAO4NhUd@xFSgRY5OpNjEub8njb?gUVOzTq8XUwen?PzBxdOrXcBVX@9"',
}

response = requests.get(amazon_url, headers=amazon_custom_headers, cookies=amazon_cookies)
soup = BeautifulSoup(response.text, "html.parser")
    
# Extraction du titre
title_element = soup.select_one("#productTitle")
if title_element:
    title = title_element.text.strip()
    print(f"Amazon Title: {title}")
else:
    print("Amazon Product title not found")
    
# Extraction de la note
rating_element = soup.select_one("#acrPopover")
if rating_element and rating_element.attrs.get("title"):
    rating_text = rating_element.attrs.get("title")
    print(f"Amazon Rating: {rating_text}")
else:
    print("Amazon Rating not found")

# Extraction du prix
price_element = soup.select_one("span.a-offscreen")
if price_element:
    price = price_element.text.strip()
    print(f"Amazon Price: {price}")
else:
    print("Amazon Price not found")

# Extraction de l'image
image_element = soup.select_one("#landingImage")
if image_element:
    image_url = image_element.attrs.get("src")
    print(f"Amazon Image URL: {image_url}")
else:
    print("Amazon Image URL not found")

# Extraction de la description
description_element = soup.select_one("#feature-bullets")
if description_element:
    description = description_element.text.strip()
    print(f"Amazon Description: {description}")
else:
        print("Amazon Description not found")