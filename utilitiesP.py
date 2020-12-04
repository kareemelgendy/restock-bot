
import requests
import json

from inputP import getProdType

# Function that loads the products json file
def loadProd(prod_url):

    web_json = prod_url + '.json'
    prod_handle = prod_url.split('products/')[1].lower()
    website = requests.get(web_json)
    products = json.loads((website.text))

    prod_title = products['product']['title'] # Product title
    variants = products['product']['variants'] # List of product variants

    return prod_title, variants

# Function that gets the number of product variants
def getNumVariants(variants): 

    variant_count = 0
    i = 1

    for variant in variants:
        if variant['option'+str(i)] != None:
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
    xxs = ['xxs', 'xxsm', 'xxsmall']
    xs = ['xs', 'xsm', 'xsmall']
    s = ['s', 'sm', 'small']
    m = ['m', 'med', 'medium']
    l = ['l', 'lg', 'large']
    xl = ['xl', 'xlg', 'xlarge']
    xxl = ['xxl', 'xxlg', 'xxlarge']

    # Converting to universal symbol
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

    return size


# Function that gets the product's ID 
def getProdId(variants, target_type):

    # Product type
    if target_type[0] == 'item':
        item = 'default title'

    elif target_type[0] == 'clothing':
        clothing_size = target_type[1]
        clothing_colour = target_type[2]
    
    elif target_type[1] == 'footwear':
        shoe_size = target_type[1]

    target_type = target_type[0]
    
    # Checking variants
    for variant in variants:
        for i in range(1, 4):

            option = variant['option' + str(i)] # Current variant value
            option_id = variant['id'] # Product variant ID

            # If product has variants
            if option != None:

                # If the item is os ie. an accessory
                if target_type == 'item':
                    if option.lower() == item or option.lower() == 'o\/s':
                        return option_id
                
                # If the item is an article of clothing
                elif target_type == 'clothing':

                    # If clothing item only has one variant - size
                    if getNumVariants(variants) == 1: #and not found:

                        # If specified size is found
                        if formatSize(option) == formatSize(clothing_size):
                            return option_id

                    # If clothing item has two variants - size & colour
                    elif getNumVariants(variants) == 2: #and not found:

                        # If the specified size is found
                        if formatSize(option) == formatSize(clothing_size):
                
                            # Find the specified colour in the current size
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]

                                # If the product is found
                                if option.lower() == clothing_colour:
                                    return option_id              
                        
                        # If the specified colour is found
                        elif option.lower() == clothing_colour: #and not found:

                            # Find the specified size in the current colour
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]

                                # If the product is found
                                if formatSize(option) == formatSize(clothing_size):
                                    return option_id

                # If the item is footwear
                elif target_type == 'footwear':
                    
                    # If the item is found
                    if option == str(shoe_size):
                        return option_id

    print('Invalid product - error occured')
    return None
