import json
import webbrowser
import requests
from helpers import format_size


class Product:
    """
    Holds and retrieves all required product information
    @param product: basic product information
    """
    def __init__(self, product):
        self.name = ''
        self.url = product['Product URL']
        self.size = format_size(product['Size'])
        self.colour = product['Colour']
        self.profile = product['Profile']
        self.phone = product['Phone']
        self.product_id = ''
        self.variant_id = ''
        self.cart = ''
        self.get_details()


    # Gets all of the required information to watch product
    def get_details(self) -> None:
        r = requests.get(self.url + '.json')
        product = json.loads(r.text)['product']

        self.product_id = product['id']
        self.name = f"{product['title']} {'- ' + self.size if self.size else ''}".upper()
        variants = product['variants']
      
        for variant in variants:
            if format_size(variant['title']) == self.size:
                self.variant_id = variant['id']
                self.generate_cart_url()


    # Generates the cart URL for the product
    def generate_cart_url(self) -> None:
        url = self.url.split('/')
        for x in url:
            if '.' in x:
                domain = x

        self.cart = f'https://{domain}/cart/{self.variant_id}:1'


    # Checks product availability
    def is_available(self) -> bool:
        catalog = f"{self.cart.split('/cart/')[0]}/products.json?limit=5000"
        r = requests.get(catalog)
        products = json.loads(r.text)['products']

        for product in products:
            if product['id'] == self.product_id:
                variants = product['variants']
                for variant in variants:
                    if variant['id'] == self.variant_id:
                        return variant['available']
        return False


    # Opens checkout page in browser
    def open_in_browser(self) -> None:
        try:
            webbrowser.open(self.cart)
        except:
            print('Error occurred - could not open in browser.')


    # Accessor method
    def get_info(self) -> tuple[str]:
        return self.name, self.variant_id, self.cart, self.profile, self.phone
