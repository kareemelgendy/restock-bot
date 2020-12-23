
import time

from utilitiesP import check_availability
from checkout import checkout_prod
from notify import notify_user

# Checks saved products availability every minute
def watch_products(profile_dict, product_dict, product_name):

    while True:
        if not product_dict.is_empty():

            for product in product_dict.get_dict():
                url = product_dict.get_val(product, 'Product URL')
                pid = product_dict.get_val(product, 'Product ID')
                vid = product_dict.get_val(product,'Variant ID')

                available = check_availability(url, pid, vid)

                # Product back in stock
                if available:
                    print('\tProduct: ' + str(product) + ' is back in stock')

                    cart_url = product_dict.get_val(product,'Cart URL')
                    profile_name = product_dict.get_val(product,'Profile')
                    phone = product_dict.get_val(product,'Notification')

                    # If user set a profile for the product
                    if profile_name != None:
                        checkout_prod(cart_url, profile_name, profile_dict)

                        email = profile_dict.get_val(profile_name, 'Email')
                        number = profile_dict.get_val(profile_name, 'Phone')
                        message = str(product) + " check out attempted. Check " + str(email)
                        
                        notify_user(number, message)

                    elif phone != None:
                        number = product_dict.get_val(product, 'Notification')
                        message = str(product) + " is back in stock.\nPress the link below to purchase:\n" + str(cart_url)
                        notify_user(number, message)

                    # Remove product after checkout attempt
                    product_dict.remove_product(product)
                    print(str(product) + ' now removed from watchlist')

                else:
                    print('\tProduct: ' + str(product) + ' not in stock')
        else:

            print('Watchlist is empty - quitting now')
            break

        time.sleep(60) # Check availability every x seconds
