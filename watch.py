
import time
from utilities import check_availability
from checkout import shopify_checkout
from notify import notify_user

# Checks saved products availability every minute
def watch_products(profile_dict, product_dict):

    # Checkout class
    checkout = shopify_checkout()

    while True:
        if not product_dict.is_empty():
            # For each product in watchlist
            for product in product_dict.get_dict():
                url = product_dict.get_val(product, 'Product URL')
                pid = product_dict.get_val(product, 'Product ID')
                vid = product_dict.get_val(product,'Variant ID')

                availability = check_availability(url, pid, vid)

                # Product back in stock
                if availability == True:
                    print('\t{} Product: {} is back in stock'.format('\u2705', product))

                    cart_url = product_dict.get_val(product,'Cart URL')
                    profile_name = product_dict.get_val(product,'Profile')
                    phone = product_dict.get_val(product,'Notification')

                    # If user set a profile for the product
                    if phone != None:
                        # Update the user - SMS
                        try:
                            number = product_dict.get_val(product, 'Notification')
                            message = '{} {} is back in stock.\nPress the link below to purchase:\n {}'.format('\U0001f6cd', product, cart_url)    
                            notify_user(number, message)  

                        except:
                            print('\t\t{} SMS could not be sent'.format('\u26A0'))

                    # If user set a number for notifications
                    elif profile_name != None:
                        # Checkout the product
                        checkout.checkout_prod(cart_url, profile_name, profile_dict)

                        # Update the user - SMS
                        try:
                            email = profile_dict.get_val(profile_name, 'Email')
                            number = profile_dict.get_val(profile_name, 'Phone')
                            message = '\t{} {} check out attempted. Check {}'.format('\U0001f6d2', product, email)
                            notify_user(number, message)

                        except:
                            print('\t\t{} SMS could not be sent'.format('\U0001f534')) 

                    # Remove product after checkout attempt
                    product_dict.remove_product(product)
                    print('\t\t{} {} now removed from watchlist'.format('\U0001f535', product))

                elif availability == False:
                    print('\t{} Product: {} not in stock'.format('\U0001f449', product))

                else:
                    product_dict.remove_product(product)
                    print('\t{} Error occured while watching - {}'.format('\U0001f534', product))
                    print('\t\t{} {} removed from watchlist'.format('\U0001f535', product))

        else:
            print('\n{} No products being watched. Quitting now...'.format('\U0001F44B'))
            quit()

        time.sleep(60) # Check availability every x seconds
