from .ceneo_scrapper import get_list_of_products, search_item_offers


class Search:
    def __init__(self, queries=[], quantities=[], options="", products=[], product_selected=[], offers_list=[], is_search_end=False):
        self.products = products
        self.options = options
        self.quantities = quantities
        self.queries = queries
        self.product_selected = product_selected
        self.offers_list = offers_list

        self.is_search_end = is_search_end

    def search_for_queries(self, queries: list, quantities: list):
        self.queries = queries
        self.quantities = quantities
        for query in self.queries:
            product_list = get_list_of_products(query, False)  # get_lower_price set to False for testing
            self.products.append(product_list)

        self.product_selected = [-1 for product_offer in self.products]
        self.is_search_end = True

    def get_product_offers(self, product_id) -> list[dict]:
        if not self.products:
            raise ValueError("Offers list is empty!")
        try:
            offers = self.products[product_id]
        except IndexError:
            raise ValueError("Index must be between 0 and " + str(len(self.products) - 1))
        return offers

    def set_selected_product(self, product_id, option):
        self.product_selected[product_id] = option

    def is_option_selected_for_all(self):
        if -1 in self.product_selected:
            return False
        return True

    def get_first_unselected_product_id(self):
        return self.product_selected.index(-1)

    def get_products_by_options(self):
        if self.is_option_selected_for_all():
            products = []
            for i, product_offers in enumerate(self.products):
                products.append(product_offers[self.product_selected[i]])
            return products

        raise ValueError("Products are not selected")

    def set_sorting_option(self, option):
        if option == 'price':
            self.options = 'price'
        elif option == 'stores':
            self.options = 'stores'
        else:
            self.options = []
            raise ValueError("Option can only be price or stores")

    def get_offers_by_option(self):
        self.offers_list =[]
        for product in self.get_products_by_options():
            offer_list = search_item_offers(product['product_id'])
            self.offers_list.append(offer_list)
        if self.options == "price":
            print(self.offers_list)
            return [offers[0] for offers in self.offers_list]
        raise ValueError("Option is not selected")

    @staticmethod
    def from_json(json_dct):
        return Search(json_dct['queries'],
                      json_dct['quantities'], json_dct['options'],
                      json_dct['products'], json_dct['product_selected'], json_dct['offers_list'], json_dct['is_search_end'])
