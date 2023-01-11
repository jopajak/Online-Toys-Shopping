from .ceneo_scrapper import get_list_of_products


class Search:
    def __init__(self):
        self.queries = []
        self.quantities = []
        self.options = []
        self.items_offers = []
        self.is_search_end = False

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
