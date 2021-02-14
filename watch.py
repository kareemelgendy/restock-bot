
import time
from utilities import check_availability
from checkout import checkout_prod
from notify import notify_user

# Checks saved products availability every minute
def watch_products(profile_dict, product_dict):

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
                    print(f'\t{'\u2705'} Product: {product} is back in stock')

                    cart_url = product_dict.get_val(product,'Cart URL')
                    profile_name = product_dict.get_val(product,'Profile')
                    phone = product_dict.get_val(product,'Notification')

                    # If user set a profile for the product
                    if phone != None:

                        # Update the user - SMS
                        try:
                            number = product_dict.get_val(product, 'Notification')
                            notify_user(number, message)
                            message = f'{'\U0001f6cd'} {product} is back in stock.\nPress the link below to purchase:\n {cart_url}'                            
                        except:
                            print(f'\t\t{'\u26A0'} SMS could not be sent')


                    # If user set a number for notifications
                    elif profile_name != None:

                        # Checkout the product
                        checkout_prod(cart_url, profile_name, profile_dict)

                        # Update the user - SMS
                        try:
                            email = profile_dict.get_val(profile_name, 'Email')
                            number = profile_dict.get_val(profile_name, 'Phone')
                            notify_user(number, message)
                            message = f'\t{'\U0001f6d2'} {product} check out attempted. Check {email}'

                        except:
                            print(f'\t\t{'\U0001f534'} SMS could not be sent') 

                    # Remove product after checkout attempt
                    product_dict.remove_product(product)
                    print(f'\t\t{'\U0001f535'} {product} now removed from watchlist')

                elif availability == False:
                    print(f'\t{'\U0001f449'} Product: {product} not in stock')

                else:
                    product_dict.remove_product(product)
                    print(f'\t{'\U0001f534'} Error occured while watching - {product}')
                    print(f'\t\t{'\U0001f535'} {product} removed from watchlist')

        else:
            print(f'\n{'\U0001F44B'} No products being watched. Quitting now...')
            quit()

        time.sleep(60) # Check availability every x seconds
