from .ceneo_scrapper import get_list_of_products, search_item_offers


class Search:
    def __init__(self, queries=[], quantities=[], sort_option="", products=[], product_selected=[], offers_list=[], is_search_end=False):
        self.products = products
        self.sort_option = sort_option
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

    def get_product_suggestions(self, product_id) -> list[dict]:
        if not self.products:
            raise ValueError("Offers list is empty!")
        try:
            products = self.products[product_id]
        except IndexError:
            raise ValueError("Index must be between 0 and " + str(len(self.products) - 1))
        return products

    def set_selected_product(self, product_id, option):
        self.product_selected[product_id] = option

    def is_option_selected_for_all(self) -> bool:
        if -1 in self.product_selected:
            return False
        return True

    def get_first_unselected_product_id(self) -> int:
        return self.product_selected.index(-1)

    def get_products_by_options(self) -> list[dict]:
        if self.is_option_selected_for_all():
            products = []
            for i, product_offers in enumerate(self.products):
                products.append(product_offers[self.product_selected[i]])
            return products

        raise ValueError("Products are not selected")

    def set_sorting_option(self, option):
        if option == 'price':
            self.sort_option = 'price'
        elif option == 'shops':
            self.sort_option = 'shops'
        else:
            self.sort_option = []
            raise ValueError("Option can only be price or stores")

    def get_offers_by_price(self) -> list[list[dict]]:
        self.offers_list = []
        for product in self.get_products_by_options():
            offer_list = search_item_offers(product['product_id'])
            self.offers_list.append(offer_list)
        if self.sort_option == 'price':
            return self.offers_list
        raise ValueError("Option is not selected")

    def get_offers_by_shops(self):
        self.offers_list = []
        for product in self.get_products_by_options():
            offer_list = search_item_offers(product['product_id'])
            self.offers_list.append(offer_list)
        if self.sort_option == 'shops':
            return self.sort_by_shop()

    def sort_by_shop(self) -> dict[str:list[dict]]:
        # returns {'shop1_name': [offer1_in_shop1,...], 'shop2_name': [...]}
        temp_offers_list = self.offers_list
        best_shop_offer = {}    # final dict with shops offers
        for product_no in range(len(self.offers_list)):
            shop_offers = {}
            # create dict where the key is 'shop_name' and the value is list of product offers in this shop
            for i, offers in enumerate(temp_offers_list):
                for offer in offers:
                    shop_name = offer['shop_name']

                    if shop_name in shop_offers:
                        shop_offers[shop_name][i] = offer
                    else:
                        shop_offers[shop_name] = [offer if j == i else None for j in range(len(temp_offers_list))]

            # now shop_offers is a dict where value is a list that contains products on the corresponding positions
            # and on other positions the value None
            best_shop = min(shop_offers, key=lambda x: (len([offer for offer in shop_offers[x] if offer is None]),
                                                        sum(offer['full_price'] for offer in shop_offers[x] if offer is not None)))

            # save best shop offer to the dict
            best_shop_offer[best_shop] = [offer for offer in shop_offers[best_shop] if offer is not None]

            # deletion of product offers that have been selected
            for x, offer in enumerate(shop_offers[best_shop]):
                if offer is not None:
                    temp_offers_list[x] = None
            temp_offers_list = [offer for offer in temp_offers_list if offer is not None]

            # check that all products have been selected
            if len(temp_offers_list) == 0:
                break

        return best_shop_offer

    @staticmethod
    def from_json(json_dct):
        return Search(json_dct['queries'],
                      json_dct['quantities'], json_dct['sort_option'],
                      json_dct['products'], json_dct['product_selected'], json_dct['offers_list'], json_dct['is_search_end'])
