from .ceneo_scrapper import get_list_of_products


class Search:
    def __init__(self, queries=[], quantities=[], options=[], products_offers=[], products_offer_selected=[], is_search_end=False):
        self.products_offers = products_offers
        self.options = options
        self.quantities = quantities
        self.queries = queries
        self.products_offer_selected = products_offer_selected

        self.is_search_end = is_search_end

    def search_for_queries(self, queries: list, quantities: list):
        self.queries = queries
        self.quantities = quantities
        for query in self.queries:
            product_offers = get_list_of_products(query, False)  # get_lower_price set to False for testing
            self.products_offers.append(product_offers)

        self.products_offer_selected = [-1 for product_offer in self.products_offers]
        self.is_search_end = True

    def get_product_offers(self, product_id) -> list[dict]:
        if not self.products_offers:
            raise ValueError("Offers list is empty!")
        try:
            offers = self.products_offers[product_id]
        except IndexError:
            raise ValueError("Index must be between 0 and " + str(len(self.products_offers) - 1))
        return offers

    def set_option(self, product_id, option):
        self.products_offer_selected[product_id] = option

    def is_option_selected_for_all(self):
        if -1 in self.products_offer_selected:
            return False
        return True

    def get_first_unselected_product_id(self):
        return self.products_offer_selected.index(-1)

    def get_offers_by_options(self):
        if self.is_option_selected_for_all():
            offers = []
            for i, product_offers in enumerate(self.products_offers):
                offers.append(product_offers[self.products_offer_selected[i]])
            return offers

        raise ValueError("Options are not selected")

    @staticmethod
    def from_json(json_dct):
        return Search(json_dct['queries'],
                      json_dct['quantities'], json_dct['options'],
                      json_dct['products_offers'], json_dct['products_offer_selected'], json_dct['is_search_end'])
