import os

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Firefox(service=Service(os.path.abspath("D:\geckodriver\geckodriver-v0.35.0-win64\geckodriver.exe"), options=chrome_options))
#chrome_options.add_argument('headless')


PAGE_URL = "https://www.technodom.kz/catalog/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki?sorting=price%3Aasc"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Content-Length": "63",
    "Content-Type": "application/json",
    "Host": "abtesting-manage-ecom.technodom.kz",
    "Origin": "https://www.technodom.kz",
    "Priority": "u=4",
    "Referer": "https://www.technodom.kz/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
    }


# def start_parser_1():
#     driver = webdriver.Firefox(options=chrome_options)
#     driver.get(url=PAGE_URL)
#     html = driver.page_source
#     soup = bs(html, "lxml")
#     products = []
#     for div in soup.find_all("div", class_="ProductCardV_card__xHsl_ ProductItem_product__hZy7p"):
#         title = div.find_next("p", class_="Typography ProductCardV_title__U38HX ProductCardV_loading___io2a Typography__M")
#         price = div.find_next("p", class_="Typography ProductCardPrices_price__oCsLy Typography__Subtitle")
#         if price is not None:
#             products.append(
#                 {
#                     "name": title.get_text().replace("/", "|"),
#                     "price": float(price.get_text().replace("₸", "").replace('\xa0', ""))
#                 }
#             )
#     driver.close()
#     driver.quit()
#     return products


def start_parser():
    page = requests.get(url=PAGE_URL)
    html = page.text

    soup = bs(html, "html.parser")
    products = []

    for div in soup.find_all("div", class_="ProductCardV_card__xHsl_ ProductItem_product__hZy7p"):
        title = div.find_next("p", class_="Typography ProductCardV_title__U38HX ProductCardV_loading___io2a Typography__M")
        price = div.find_next("p", class_="Typography ProductCardPrices_price__oCsLy Typography__Subtitle")
        if price is not None:
            products.append(
                {
                    "name": title.get_text().replace("/", "|"),
                    "price": float(price.get_text().replace("₸", "").replace('\xa0', ""))
                }
            )
    return products


if __name__ == "__main__":
    start_parser()
