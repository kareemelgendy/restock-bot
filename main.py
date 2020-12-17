
import webbrowser

from profileDict import Profile
from productDict import Product

from inputP import getProdType, getCartNum, retryEntry, getWatchOption
from utilitiesP import getProduct, getNumVariants, getVariantInfo, checkAvailability, formatSize, getCartLink
from outputP import printHeader, printResult

# Initializing the dictionaries
profile_dict = Profile()
product_dict = Product()

# Banner
printMainHeader()

# Getting the url from the user
prod_url = input('\nInsert Product URL: ')
product = getProduct(prod_url)

prod_title = product['product']['title'] # Product Title
prod_id = product['product']['id'] # Product ID
prod_options = product['product']['variants'] # List of product variants

target_prod = getProdType()
variant_id = getVariantInfo(prod_options, target_prod)
available = checkAvailability(prod_url, prod_id, variant_id)

product_type = target_prod[0]

if available:
    status = 'In Stock'
else:
    status = 'Out of Stock'

# If a product was found 
if variant_id != None:
    # Printing product specifications
    printResultHeader()
    print('Product Name: ' + str(prod_title))

    # Print the options 
    if product_type == 'clothing':        
        clothing_size = formatSize(target_prod[1]).upper()
        clothing_colour = target_prod[2]
        print('Product Size: ' + str(clothing_size))
        print('Product Colour: ' + str(clothing_colour).title())
    elif product_type == 'shoes':
        print('Product Size: ' + str(clothing_size).upper())

    print('Product ID: ' + str(prod_id))
    print('Variant ID: ' + str(variant_id))
    print('Availability: ' + str(status))
    print('---------------------------------')

    # If the product is in stock
    if available:
        num_items = getCartNum()
        cart_url = getCartLink(prod_url, variant_id, num_items)
        
        # Opening cart in browser
        print('\nAdding product to cart, one moment.')
        webbrowser.open_new(cart_url)
        print('Task completed.\n')
        quit()

    else:
        print('\nProduct not in stock')
        cart_url = getCartLink(prod_url, variant_id, 1)
        getWatchOption(profile_dict, product_dict, prod_title, prod_id, variant_id, cart_url)

        # run availability check here

# If product was not found or invalid entry
else:
    retryEntry(prod_id)