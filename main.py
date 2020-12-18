
import webbrowser

from profileDict import Profile
from productDict import Product
from outputP import *
from inputP import *
from utilitiesP import *
from watch import *

# Main program
def main():
    # Getting the url from the user
    prod_url = input('\nInsert Product URL: ')
    product = get_product(prod_url)

    # Validate URL
    if product != False:
        prod_title = product['product']['title'] # Product Title
        prod_id = product['product']['id'] # Product ID
        prod_options = product['product']['variants'] # List of product variants

        try:
            target_prod = get_prod_type() # Product type
            var_id = get_variant_id(prod_options, target_prod) # 
            available = check_availability(prod_url, prod_id, var_id)
            cart_url = get_cart_link(prod_url, var_id)
            product_type = target_prod[0]

            # Product in stock
            if available:
                print('\n-------- Product in stock --------')

                # Opening cart in browser
                print('\nAdding product to cart, one moment.')
                webbrowser.open_new(cart_url)
                print('Task completed.\n')

                # No products being watched
                if prod_dict.is_empty():
                    quit()
                else: 
                    watch_products(profile_dict, prod_dict, prod_title)

            # Product not in stock
            else:
                print('\n-------- Product out of stock --------')
                
                if get_watch_option():
                    prod_dict.new_product(prod_title) ## Adding product to watchlist    
                    prod_dict.set_val(prod_title, 'Product URL', prod_url)
                    prod_dict.set_val(prod_title, 'Product ID', prod_id)
                    prod_dict.set_val(prod_title, 'Variant ID', var_id)
                    prod_dict.set_val(prod_title, 'Cart URL', cart_url)

                    if get_auto_checkout(profile_dict):
                        create_profile(profile_dict, prod_dict, prod_title)

                        if get_new_prod(prod_dict):
                            main()
        
        except:
            print('\nError occured.')
            print('Make sure all entries are valid.')

            if get_new_prod(prod_dict):
                main()

        if not prod_dict.is_empty():
            watch_products(profile_dict, prod_dict, prod_title)
        else:
            quit()
    else:
        print('call menu')

# Initializing the dictionaries
profile_dict = Profile()
prod_dict = Product()

# Banner
print_banner() 

# Running main program
main()
