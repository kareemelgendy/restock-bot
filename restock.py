#from selenium import webdriver
import requests
import json
import time

# 1 variant getting one size up
# footwear not tested yet
# items not tested yet

def getNumVariants(variants):
    variant_count = 0
    i = 1
    for variant in variants:
        if variant['option'+str(i)] != None:
            variant_count += 1
        else:
            break
        i+=1
    return variant_count

def formatSize(size):

    # Formatting the size
    size = size.replace('-', '').lower()

    # list of all sizes and possibilities
    xxs = ['xxs', 'xxsm', 'xxsmall']
    xs = ['xs', 'xsm', 'xsmall']
    s = ['s', 'sm', 'small']
    m = ['m', 'med', 'medium']
    l = ['l', 'lg', 'large']
    xl = ['xl', 'xlg', 'xlarge']
    xxl = ['xxl', 'xxlg', 'xxlarge']

    # checking 
    if size[0] == 'x':
        if size in xxs:
            size = 'xxs'
        elif size in xs:
            size = 'xs'
        elif size in xl:
            size = 'xl'
        elif size in xxl:
            size = 'xxl'
    
    else:
        if size[0] == 's':
            size = 's'
        elif size[0] == 'm':
            size = 'm'
        elif size[0] == 'l':
            size = 'l'
        else:
            print('Error - size issue')

    return size

# Number of items to cart
def getCartNum(product_type):
    try:
        print('How many ' + product_type.lower() + 's would you like to cart?')
        num_items = int(input('Enter number (Recommended 1): '))
        return num_items

    except ValueError:
        print("Invalid input - please enter a valid whole number.")
        getCartNum(product_type)

# Confirm the right product has been found
def sendConf(prod_url, prod_id, num_items):

    print('Product Found')
    # print product info - title, id, 

    confirmation = input('Would you like to open a webpage to confirm the right product is being watched? (y/n): ')

    if confirmation == 'y':

        # Print product 

        cart_url = prod_url.split('.com')[0] + '.com/cart/update?updates[' + str(prod_id) + ']=' + str(num_items)
        item_url = prod_url + '?variant' + str(prod_id)
        print('Cart link: ' + (cart_url))
        print('Product page link: ' + (item_url))
        #driver = webdriver.Chrome('./chromedriver')
        #driver.get(item_url)

    elif confirmation == 'n':
        print('Item being watched')
        print(cart_url)

    # Invalid input
    else:
        print('\nInvalid input')
        sendConf(prod_url, prod_id, num_items)
    

# Function that gets the product's ID 
def getProdId(variants):
    clothing_cl = False
    clothing_sz = False
    found = False
    
    # Checking variants
    for variant in variants:

        for i in range(1, 4):

            option = variant['option' + str(i)]
            option_id = variant['id']

            # If product has variants
            if option != None:

                # If the item is os ie. an accessory
                if option.lower() == 'default title':
                    prod_id = option_id
                    break
                
                # If the item is an article of clothing
                elif target_type == 'clothing':

                    # If clothing item only has one variant - size
                    if getNumVariants(variants) == 1:

                        # If desired size is found
                        if formatSize(option) == clothing_size:
                            clothing_sz = True
                            clothing_cl = True
                            prod_id = option_id
                            break
                        else:
                            print('wrong size')

                    # If clothing item has two variants - size & colour
                    elif getNumVariants(variants) == 2:

                        # If the specified size is found
                        if formatSize(option) == clothing_size:
                            
                            # Find the specified colour in the current size
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]

                                # If product found
                                if option.lower() == clothing_colour:
                                    clothing_cl = True
                                    clothing_sz = True
                                    prod_id = option_id
                                    break
                                else:
                                    print('wrong size')
                        
                        # If the specified colour is found
                        elif option.lower() == clothing_colour:

                            # Find the specified size in the current colour
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]

                                # If product found
                                if formatSize(option) == clothing_size:
                                    clothing_sz = True
                                    clothing_cl = True
                                    prod_id = option_id
                                    break
                                else:
                                    print('wrong size')

                    # If both colour and size found
                    if clothing_sz and clothing_cl:
                        print('PROD ID ---------------> ' + str(option_id))
                        prod_id = option_id
                        found = True
                        break

                elif found:
                    break
                    
                # If item is footwear
                elif target_type == 'footwear':
                    if option == str(shoe_size):
                        shoe_sz = True
                        prod_id = option_id
                        break
                    else: 
                        print('shoe size not found')
        if found:
            break

    return option_id
                    
########################################################################

print('----------------------------------------------------------')
print('                  Welcome to Restock Bot                  ')
print('----------------------------------------------------------')
print('Product types supported (clothing, footwear, item):')
print('-Clothing items with letter sizing and/or colour options')
print('-OS options such as accessories (not variants)')
print('-Footwear with number size options')
print('----------------------------------------------------------')

# Get the product type
print("Enter one of the following ('clothing', 'footwear', or 'item'")
target_type = input('\nEnter Product Type (q to quit): ').lower()

# Check the target product type
if target_type.lower() == 'clothing':
    clothing_size = input('\nEnter Clothing Size: ').lower()
    clothing_colour = input('\nEnter Colour: ').lower()

elif target_type.lower() == 'footwear':
    shoe_size = input('\nEnter Shoe Size: ').lower()

elif target_type.lower() == 'item':
    one_size = True
    # enter function to call info

elif target_type.lower() == 'q':
    quit()

else:
    print('Invalid input - quitting')
    quit()

########################################################################

# Getting the product URL
prod_url = input('Insert Product URL: ')

# Loading the product's json file
web_json = prod_url + '.json'
prod_handle = prod_url.split('products/')[1].lower()
website = requests.get(web_json)
products = json.loads((website.text))

# List of product variants
variants = products['product']['variants']

# Product type
product_type = products['product']['product_type']

target_product_id = getProdId(variants)
num_items = getCartNum(product_type)

if target_product_id != False:
    getCartNum(product_type)
    sendConf(prod_url, target_product_id, num_items)

else:
    print('\nBot Failed')
    print('\nMake sure to enter a valid/live product url')

########################################################################
