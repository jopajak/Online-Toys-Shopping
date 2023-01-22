from app.app import celery
from app.ceneo_scrapper import get_list_of_products


@celery.task
def request_for_product(queries):
    products = []
    for query in queries:
        product_list = get_list_of_products(query, False)  # get_lower_price set to False for testing
        products.append(product_list)
    return products
