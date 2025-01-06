import requests
from bs4 import BeautifulSoup

ebay_url = "https://www.ebay.com/itm/315871566918?_trkparms=amclksrc%3DITM%26aid%3D1110018%26algo%3DHOMESPLICE.COMPLISTINGS%26ao%3D1%26asc%3D264184%26meid%3D8cd57dce6bf34c78917d7a783cf0afbf%26pid%3D101196%26rk%3D2%26rkt%3D12%26sd%3D387743508213%26itm%3D315871566918%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DCompVIDesktopATF2V6&_trksid=p2332490.c101196.m2219&itmprp=cksum%3A3158715669188cd57dce6bf34c78917d7a783cf0afbf%7Cenc%3AAQAJAAABMLx1mZQ2L9jLv%252BUPTFTna8XcGfl2wNJcn022gtZb5sDiFrTi3gwMo%252Fa--7j5u2kQDPo58ZnaS782LdgqLI9am6jY%252FLT0qkSl5rcxT2rvJwfU%252BP88LLNs7p%252Fy12EYYq1k2CU1vc5GX4zQMEyhHPS8rxUz%252F6msFUnNf9xRDCd7Jhd0x7%252FZfMQx9GP8bL9RkF8%252BJFU4JmgC8v%252FGamZw6wCQs8aylUjbSrxZDrKrVygA67eAfI2YJeviejXcQdhmFj%252BPFsP94jiXzteWDqyBxJ5hJOul4SRN6IAsWnR%252F5UfmCuwP2HjbNjR5s0lq%252Bq%252BcopgnZKonD7W564tHzVHM5StDd6l0mshxWPRIMb2ZmkQLFnCqYGw9h5nqjBiIvgvoYC%252F2RjqxKVNTMdw6EULOKrRPgEk%253D%7Campid%3APL_CLK%7Cclp%3A2332490&itmmeta=01JGYHPRMS7C3DJNRFP519G1BA"

ebay_custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

#ebay_cookies = {
 #   'session-id': 'your-session-id',
  #  'user-info': 'some-cookie-value',
#}

response = requests.get(ebay_url, headers=ebay_custom_headers)#, cookies=ebay_cookies)
soup = BeautifulSoup(response.text, "html.parser")
    
# Extraction du titre
title_element = soup.select_one("#ux-textspans ux-textspans--BOLD")
if title_element:
    title = title_element.text.strip()
    print(f"eBay Title: {title}")
else:
    print("eBay Product title not found")
    
# Extraction de la note
rating_element = soup.select_one("#fdbk-detail-seller-rating__value")
if rating_element:
    rating_text = rating_element.text.strip()
    print(f"eBay Rating: {rating_text}")
else:
    print("eBay Rating not found")

# Extraction du prix
price_element = soup.select_one("#span.x-bin-price")
if price_element:
    price = price_element.text.strip()
    print(f"eBay Price: {price}")
else:
    print("eBay Price not found")

# Extraction de l'image
image_element = soup.select_one("#ux-image-carousel-item image-treatment active  image")
if image_element:    
    image_url = image_element.attrs.get("src")
    print(f"eBay Image URL: {image_url}")
else:
    print("eBay Image URL not found")

# Extraction de la description
description_element = soup.select_one("#d-item-description")
if description_element:
    description = description_element.text.strip()
    print(f"eBay Description: {description}")
else:
    print("eBay Description not found")