import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, product_id="", name="", price=0.0):
        self.product_id = product_id
        self.name = name
        self.price = price


class Offer:
    def __init__(self, shop_name, shop_link, full_price):
        self.shop_name = shop_name
        self.shop_link = 'www.ceneo.pl' + shop_link
        self.full_price = full_price


def get_list_of_products(search_text, get_lowest_price) -> list:
    if get_lowest_price:
        url_link = 'https://www.ceneo.pl/szukaj-' + search_text + ';0112-0.htm'  # filtr od najmniejszej ceny
    else:
        url_link = 'https://www.ceneo.pl/szukaj-' + search_text

    html_text = requests.get(url_link)
    soup = BeautifulSoup(html_text.text, 'lxml')
    # dwa rodzaje elementów jakie mogą się pojawić
    elements1 = soup.find_all('div',
                              class_='cat-prod-row js_category-list-item js_clickHashData js_man-track-event')
    elements2 = soup.find_all('div',
                              class_='cat-prod-row js_category-list-item js_clickHashData js_man-track-event js_redirectorLinkData')
    elements = elements1 + elements2
    products = []

    for element in elements:
        name = element.get('data-productname')
        price = element.get('data-productminprice')
        product_id = element.get('data-productid')
        products.append(Product(product_id=product_id, name=name, price=float(price)))

    products.sort(key=lambda x: x.price)
    products = products[:10]
    return [vars(product) for product in products]  # change product type from Product object to dict


def search_item_offers(product_id):
    url_link = 'https://www.ceneo.pl/' + product_id + ';0280-0.htm'
    html_text = requests.get(url_link)
    soup = BeautifulSoup(html_text.text, 'lxml')

    total_elements = soup.find_all('div', 'product-offer js_full-product-offer')

    offers = []

    for element in total_elements:
        details = element.find('div',
                               class_='product-offer__container clickable-offer js_offer-container-click js_product-offer')
        if details is not None:
            shop_name = details.get('data-shopurl')
            shop_link = details.get('data-click-url')
            final_price = 0.0
            product_price = details.get('data-price')
            delivery_price_txt = str(details.find('span', class_='product-delivery-info js_deliveryInfo')
                                     .get_text().strip('\n'))
            if delivery_price_txt.__contains__('wysyłką'):
                string_list = delivery_price_txt.split('\n')
                price_d = float(string_list[1].strip(' zł').replace(',', '.'))
                final_price = price_d
            elif delivery_price_txt.__contains__('Darmowa'):
                final_price = float(product_price)

            # ignorujemy allegro
            if shop_name == 'allegro.pl':
                continue

            offers.append(Offer(shop_name=shop_name, shop_link=shop_link, full_price=final_price))

        # tutaj inny web scraping dla ofert, które pochodzą od sprzedawców zarejestrowanych na ceneo (czyli nie tych
        # z zewnątrz jak amazon itp.)
        else:
            details = element.find('div', class_='product-offer__container js_product-offer')
            shop_name = element.find('a', class_='link js_product-offer-link').get_text().strip('\n').split(' ')[-1]
            shop_link_txt = details.find('button', class_='button button--primary button--flex add-to-basket-no-popup')
            shop_link = '/' + shop_link_txt.get('data-product') + ';' + shop_link_txt.get('data-shop') + '-0v.htm'
            final_price = 0.0

            delivery_price_txt = str(
                details.find('span', class_='product-delivery-info js_deliveryInfo js_hide-buy-in-shop')
                .get_text().strip('\n'))

            if delivery_price_txt.__contains__('wysyłką'):
                string_list = delivery_price_txt.split('\n')
                price_d = float(string_list[1].strip(' zł').replace(',', '.'))
                final_price = price_d
            elif delivery_price_txt.__contains__('Darmowa'):
                final_price = float(0.0)

            offers.append(Offer(shop_name=shop_name, shop_link=shop_link, full_price=final_price))

    offers.sort(key=lambda x: x.full_price)

    # tuaj możemy zwrócić pierwszą najlepszą oferte albo listę ofert
    return [vars(offer) for offer in offers]    # change product type from Offer object to dict

