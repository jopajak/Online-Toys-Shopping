from app import ceneo_scrapper


def test_get_list_of_products():
    # list of product names to test
    product_exist_list = ["Buty", "Klocki", "Lego", "Płetwy", "Obroża dla psa"]
    product_nonexist_list = ["hadshsakhsf", "", "a"]

    for product in product_exist_list:
        assert 10 == len(ceneo_scrapper.get_list_of_products(product, False))

    for product in product_nonexist_list:
        assert 0 == len(ceneo_scrapper.get_list_of_products(product, False))


def test_get_url():
    # test empty id
    assert [] == ceneo_scrapper.get_url("")
