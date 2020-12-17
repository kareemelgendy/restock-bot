
import time

from utilitiesP import checkAvailability
from checkout import checkoutProd

# Checks saved products availability every minute
def watchProducts(profile_dict, product_dict, product_name):

    while True:
        if product_dict.size() != 0:

            for product in product_dict.getDict():
                print(str(product)) #+ '------' + str(product_dict.getVal(product)))
                url = product_dict.getVal(product, 'Product URL')
                pid = product_dict.getVal(product, 'Product ID')
                vid = product_dict.getVal(product,'Variant ID')

                if checkAvailability(url, pid, vid):
                    cart_url = product_dict['Cart URL']
                    profile_name = product_dict['Profile']
                    checkoutProd(cart_url, profile_name, profile_dict)
                    product_dict.removeProduct(product)
        else:
            print('Watchlist is empty - quitting now')
            break

        time.sleep(60)
