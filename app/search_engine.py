from .ceneo_scrapper import get_list_of_products


class Search:
    def __init__(self, queries=[], quantities=[], options=[], items_offers=[], is_search_end=False):
        self.items_offers = items_offers
        self.options = options
        self.quantities = quantities
        self.queries = queries

        self.is_search_end = is_search_end

    def search_for_queries(self, queries: list, quantities: list):
        self.queries = queries
        self.quantities = quantities
        for query in self.queries:
            item = get_list_of_products(query, False)  # get_lower_price set to False for testing
            self.items_offers.append(item)
        self.is_search_end = True

    def get_item_offers(self, item_id) -> list[dict]:
        if not self.items_offers:
            raise ValueError("Offers list is empty!")
        try:
            offers = self.items_offers[item_id]
        except IndexError:
            raise ValueError("Index must be between 0 and " + str(len(self.items_offers) - 1))
        return offers

    @staticmethod
    def from_json(json_dct):
        return Search(json_dct['queries'],
                      json_dct['quantities'], json_dct['options'],
                      json_dct['items_offers'], json_dct['is_search_end'])
