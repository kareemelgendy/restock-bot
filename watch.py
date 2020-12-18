
import time

from utilitiesP import check_availability
from checkout import checkout_prod

# Checks saved products availability every minute
def watch_products(profile_dict, product_dict, product_name):

    while True:
        if not product_dict.is_empty():

            for product in product_dict.get_dict():
                url = product_dict.get_val(product, 'Product URL')
                pid = product_dict.get_val(product, 'Product ID')
                vid = product_dict.get_val(product,'Variant ID')

                available = check_availability(url, pid, vid)

                if available:
                    print('\tProduct: ' + str(product) + ' back in stock')
                    cart_url = product_dict['Cart URL']
                    profile_name = product_dict['Profile']
                    checkout_prod(cart_url, profile_name, profile_dict)
                    product_dict.remove_product(product)
                    print(str(product) + ' now removed from watchlist')
                else:
                    print('\tProduct: ' + str(product) + ' not in stock')
        else:
            print('Watchlist is empty - quitting now')
            break

        time.sleep(60) # Check availability every x seconds
