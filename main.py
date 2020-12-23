
import webbrowser

from profile_dict import Profile
from product_dict import Product
from banner import print_banner
from watch import watch_products
from user_input import *
from utilities import *

# Main program
def main(profile_dict, product_dict):
    # Getting the url from the user
    prod_url = input('\nInsert Product URL: ')
    product = get_product(prod_url) # Validate URL

    # If product exists
    if product != False:
        prod_title = product['product']['title'] # Product Title
        prod_id = product['product']['id'] # Product ID
        prod_options = product['product']['variants'] # List of product variants

        try:
            target_prod = get_prod_type() # Product type
            variant_id = get_variant_id(prod_options, target_prod) # 
            available = check_availability(prod_url, prod_id, variant_id)
            cart_url = get_cart_link(prod_url, variant_id)
            product_type = target_prod[0]

            # Product in stock
            if available:
                print('\n-------- Product in stock --------')

                # Opening cart in browser
                print('\nAdding product to cart, one moment.')
                webbrowser.open_new(cart_url)
                print('Task completed.\n')

                # No products being watched
                if product_dict.is_empty():
                    quit()
                else: 
                    print('\nWatching products...')
                    watch_products(profile_dict, product_dict, prod_title)

            # Product not in stock
            else:
                print('\n-------- Product out of stock --------')
                
                if get_watch_option():
                    print('get watch option true')
                    product_dict.new_product(prod_title) ## Adding product to watchlist    
                    product_dict.set_val(prod_title, 'Product URL', prod_url)
                    product_dict.set_val(prod_title, 'Product ID', prod_id)
                    product_dict.set_val(prod_title, 'Variant ID', variant_id)
                    product_dict.set_val(prod_title, 'Cart URL', cart_url)

                    # Automatically check out the product
                    if get_auto_checkout(profile_dict, product_dict):
                        create_profile(profile_dict, product_dict, prod_title)

                        if get_new_prod(product_dict):
                            main(profile_dict, product_dict)
                        else:
                            watch_products(profile_dict, product_dict, prod_title)

                    # Update the user when it becomes available
                    else:
                        #try:
                        print('\nThe program will notify you when the product becomes available')
                        product_dict.set_val(prod_title, 'Notification', input('Enter your phone number: '))

                        if get_new_prod(product_dict):
                            main(profile_dict, product_dict)
                        else:
                            watch_products(profile_dict, product_dict, prod_title)

                #         except:
                #             print('Error - cannot set phone number to product')
                else:
                    print('\nUser does not want to watch the product')

                    if product_dict.is_empty():
                        print('Product watchlist empty - quitting now.')
                        quit()

        except:
            if not product_dict.is_empty():
                watch_products(profile_dict, product_dict, prod_title)
            else:
                quit()
    else:
        print('Invalid URL - Product not found')

# Banner
print_banner() 

# Initializing the dictionaries
profile_dict = Profile()
product_dict = Product()

main(profile_dict, product_dict)