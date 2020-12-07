
import requests
import json

from inputP import getProdType

#def saveProduct(prod_title, prod_dict, value):

# Function that loads the products json file
def getProduct(prod_url):
    web_json = prod_url + '.json'
    prod_handle = prod_url.split('products/')[1].lower()
    website = requests.get(web_json)
    products = json.loads((website.text))

    return products

# Function that gets the number of product variants
def getNumVariants(variants): 
    variant_count = 0
    i = 1
    for variant in variants:
        if variant['option' + str(i)] != None:
            variant_count += 1
        else:
            break
        i += 1
    return variant_count

# Function that formats the clothing size
def formatSize(size):

    # Formatting the size
    size = size.replace('-', '').lower()

    # list of all sizes and possibilities
    xxs = ['xxs', 'xxsm', 'xxsmall', '2xs']
    xs = ['xs', 'xsm', 'xsmall']
    s = ['s', 'sm', 'small']
    m = ['m', 'med', 'medium']
    l = ['l', 'lg', 'large']
    xl = ['xl', 'xlg', 'xlarge']
    xxl = ['xxl', 'xxlg', 'xxlarge', '2xl']

    # Converting to universal symbol
    if size[0] == 'x' or size[0] == 2:
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

    return size

# Function that gets the product's ID 
def getVariantInfo(variants, target_prod):

    # Product type
    if target_prod[0] == 'item':
        item = 'default title'
    elif target_prod[0] == 'clothing':
        clothing_size = target_prod[1]
        clothing_colour = target_prod[2]
    elif target_prod[0] == 'footwear':
        shoe_size = target_prod[1]

    target_prod = target_prod[0]
    num_variants = getNumVariants(variants)
    
    # Checking variants
    for variant in variants:
        for i in range(1, 4):

            option = variant['option' + str(i)] # Current variant value
            variant_id = variant['id'] # Product variant ID

            # If product has variants
            if option != None:
                option = option.lower()
                # If the item is os ie. an accessory
                if target_prod == 'item':
                    if option == item or option == 'o\/s':
                        return variant_id
                
                # If the item is an article of clothing
                elif target_prod == 'clothing':
                    # If clothing item only has one variant - size
                    if num_variants == 1: #and not found:
                        # If specified size is found
                        if formatSize(option) == formatSize(clothing_size):
                            return variant_id

                    # If clothing item has two variants - size & colour
                    elif num_variants == 2: #and not found:
                        # If the specified size is found
                        if formatSize(option) == formatSize(clothing_size):
                            # Find the specified colour in the current size
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]
                                # If the product is found
                                if option == clothing_colour:
                                    return variant_id              
                        
                        # If the specified colour is found
                        elif option == clothing_colour: #and not found:
                            # Find the specified size in the current colour
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]
                                # If the product is found
                                if formatSize(option) == formatSize(clothing_size):
                                    return variant_id

                # If the item is footwear
                elif target_prod == 'footwear':
                    # If the item is found
                    if option == str(shoe_size):
                        return variant_id

    print('Product not found.')
    return None

def checkAvailability(prod_url, prod_id, var_id):

    tld = '.' + prod_url.split('/')[2].split('.')[1]
    web_json = prod_url.split(tld)[0] + tld + '/products.json?limit=1000'
    website = requests.get(web_json)
    products = json.loads((website.text))['products']

    for product in products:
        if product['id'] == prod_id:
            name = product['title']

            variants = product['variants']
            for variant in variants:
                availability = variant['available']

                if variant['id'] == var_id:
                    availability = variant['available']
                    if availability:
                        return True

    return False

def getCartLink(prod_url, variant_id, num_items):

    tld = '.' + prod_url.split('/')[2].split('.')[1]
    cart_url = prod_url.split(tld)[0] + tld + '/cart/update?updates[' + str(variant_id) + ']=' + str(num_items)
    return cart_url