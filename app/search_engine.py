from .ceneo_scrapper import get_url

from app.tasks import request_for_product, request_for_offers


class Search:
    def __init__(self, queries=[], quantities=[], sort_option="", products=[], product_selected=[], offers_list=[],
                 is_products_search_end=False, is_offers_search_end=False, last_selected_product=0, task_id=None, task_sd_id=None):
        self.queries = queries
        self.quantities = quantities
        self.sort_option = sort_option
        self.products = products
        self.product_selected = product_selected
        self.offers_list = offers_list
        self.is_products_search_end = is_products_search_end
        self.is_offers_search_end = is_offers_search_end
        self.last_selected_product = last_selected_product
        self.task_id = task_id
        self.task_sd_id = task_sd_id

    def get_product_suggestions(self, product_id: int) -> list[dict]:
        """
        Returns a list of products previously found based on a query.
        """
        if not self.products:
            raise ValueError("Offers list is empty!")
        try:
            products = self.products[product_id]
        except IndexError:
            raise ValueError("Index must be between 0 and " + str(len(self.products) - 1))
        return products

    def set_selected_product(self, product_id: int, option: int):
        """
        Sets the selected product variant for the list of found products based on the query,
        where -2 is the skipped product, -1 the default option (not set), 0-9 index the selected option.
        """
        if -2 <= option <= 9:
            self.product_selected[product_id] = option
            self.last_selected_product = product_id
            self.is_offers_search_end = False   # Any change to a product cancels the previous offer search
        else:
            raise ValueError('Option must between -2 and 9')

    def is_option_selected_for_all(self) -> bool:
        if -1 in self.product_selected or self.last_selected_product < len(self.products) - 1:
            return False
        return True

    def get_first_unselected_product_id(self) -> int:
        index = 100
        try:
            index = self.product_selected.index(-1)
        except ValueError:
            pass
        return min(self.last_selected_product + 1, index)

    def get_products_by_options(self) -> list[dict]:
        """
        Returns a list of selected products, without omitted products
        """
        if self.is_option_selected_for_all():
            products = []
            for i, product_offers in enumerate(self.products):
                if not self.product_selected[i] == -2:
                    # products that were not skipped
                    products.append(product_offers[self.product_selected[i]])
            return products

        raise ValueError("Products are not selected")

    def set_sorting_option(self, option: str):
        if option == 'price':
            self.sort_option = 'price'
        elif option == 'shops':
            self.sort_option = 'shops'
        else:
            self.sort_option = []
            raise ValueError("Option can only be price or shops")

    def get_sorting_option(self):
        return self.sort_option

    def get_offers_by_price(self) -> list[list[dict]]:
        if self.sort_option == 'price':
            return self.offers_list
        raise ValueError("Option is not selected")

    def get_offers_by_shops(self):
        if self.sort_option == 'shops':
            return self.sort_by_shop()
        raise ValueError("Option is not selected")

    def search_for_products(self, queries: list, quantities: list):
        """
        Delegates product search to a separate task
        """
        self.queries = queries
        self.quantities = quantities
        self.products = []  # without it, there was a problem that products passed between searches
        self.task_id = request_for_product.delay(queries).id
        self.is_products_search_end = False

    def check_for_searching_products(self):
        """
        A method used to check if search results from a separate task are already available
        """
        if request_for_product.AsyncResult(self.task_id).ready():
            self.products = request_for_product.AsyncResult(self.task_id).result
            self.product_selected = [-1 for _ in self.products]     # option -1 means not selected
            self.is_products_search_end = True

    def search_for_offers(self):
        """
        Delegates offers search to a separate task
        """
        if not self.is_offers_search_end:
            self.offers_list = []
            self.is_offers_search_end = False
            self.task_sd_id = request_for_offers.delay(self.get_products_by_options()).id

    def check_for_searching_offers(self):
        """
        A method for checking whether the results of a search for offers from a separate task are already available
        """
        if request_for_offers.AsyncResult(self.task_sd_id).ready():
            self.offers_list = request_for_offers.AsyncResult(self.task_sd_id).result
            self.is_offers_search_end = True

    def sort_by_shop(self) -> dict[str:list[dict]]:
        """
         A method that sorts offers so that the number of stores where offers are available is as small as possible
         and the price is as low as possible
        """
        # returns {'shop1_name': [offer1_in_shop1,...], 'shop2_name': [...]}
        temp_offers_list = self.offers_list
        best_shop_offer = {}  # final dict with shops offers
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
            def key_func(shop):
                offers = shop_offers[shop]
                shop_offers_price = sum([offer['base_price']*self.quantities[product_index]
                                         for product_index, offer in enumerate(offers) if offer is not None])
                delivery_cost = max((offer['base_price'] - offer['base_price'])
                                     for offer in offers if offer is not None)
                total_price = shop_offers_price + delivery_cost

                # Returns a tuple with two ints first compares the number of items in a store, if the number of products
                # in more than one store is the same, the total cost is compared
                return len([offer for offer in offers if offer is None]), total_price

            best_shop = min(shop_offers, key=key_func)

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

    def get_queries_length(self) -> int:
        return len(self.queries)

    @staticmethod
    def from_json(json_dct: dict):
        """
        Method that creates an object based on data read from JSON
        """
        return Search(json_dct['queries'],
                      json_dct['quantities'], json_dct['sort_option'],
                      json_dct['products'], json_dct['product_selected'], json_dct['offers_list'],
                      json_dct['is_products_search_end'], json_dct['is_offers_search_end'],
                      json_dct['last_selected_product'], json_dct['task_id'], json_dct['task_sd_id'])
