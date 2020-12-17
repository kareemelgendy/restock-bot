
import webbrowser

from profileDict import Profile
from productDict import Product
from outputP import *
from inputP import *
from utilitiesP import *
from watch import *

# Initializing the dictionaries
profile_dict = Profile()
prod_dict = Product()

# Banner
printBanner()

### ---------------------------------------------- ###

# Getting the url from the user
prod_url = input('\nInsert Product URL: ')
product = getProduct(prod_url)

# Validate URL

prod_title = product['product']['title'] # Product Title
prod_id = product['product']['id'] # Product ID
prod_options = product['product']['variants'] # List of product variants

target_prod = getProdType() # Product type
var_id = getVariantID(prod_options, target_prod) # 
available = checkAvailability(prod_url, prod_id, var_id)
cart_url = getCartLink(prod_url, var_id)

product_type = target_prod[0]

### ---------------------------------------------- ###

# If the product is in stock
if available:
    print('\n-------- Product in stock --------')

    # Opening cart in browser
    print('\nAdding product to cart, one moment.')
    webbrowser.open_new(cart_url)
    print('Task completed.\n')

    if dict.size() == 0:
        quit()
    else: 
        watchProducts(profile_dict, prod_dict, prod_name)

else:
    print('\n-------- Product out of stock --------')
    
    if getWatchOption():
        prod_dict.newProduct(prod_title) ## Adding product to watchlist    
        prod_dict.setVal(prod_title, 'Product URL', prod_url)
        prod_dict.setVal(prod_title, 'Product ID', prod_id)
        prod_dict.setVal(prod_title, 'Variant ID', var_id)
        prod_dict.setVal(prod_title, 'Cart URL', cart_url)

        if getAutoCheckout(profile_dict):
            createProfile(profile_dict, prod_dict, prod_title)

            if getNewProd(prod_dict):
                print('run program again') ##########

if prod_dict.size() >= 1:
    watchProducts(profile_dict, prod_dict, prod_title)

else:
    quit()