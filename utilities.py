
import requests, json
from inputP import get_prod_type

# Function that loads the products json file
def get_product(prod_url):

    try:
        print(requests.get(prod_url).status_code)

        #If a variant is in the url
        if len(prod_url.split('?')) > 1:
            prod_url = prod_url.split('?')[0]

        web_json = prod_url + '.json'
        prod_handle = prod_url.split('products/')[1].lower()

        website = requests.get(web_json)
        products = json.loads((website.text))

        return products
    
    except:
        print('Invalid URL entered')
        return False

# Returns the number of product variants
def get_num_variants(variants): 
    variant_count = 0
    i = 1
    for variant in variants:
        if variant['option' + str(i)] != None:
            variant_count += 1
        else:
            break
        i += 1
    return variant_count

# Formats the clothing size
def format_size(size):

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
        else:
            return None

    return size

# Function that gets the product's ID 
def get_variant_id(variants, target_prod):

    # Product type
    if target_prod[0] == 'item':
        item = 'default title'
    elif target_prod[0] == 'clothing':
        clothing_size = target_prod[1]
        clothing_colour = target_prod[2]
    elif target_prod[0] == 'footwear':
        shoe_size = target_prod[1]

    target_prod = target_prod[0]
    num_variants = get_num_variants(variants)
    
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
                        if format_size(option) == format_size(clothing_size):
                            return variant_id

                    # If clothing item has two variants - size & colour
                    elif num_variants == 2: #and not found:
                        # If the specified size is found
                        if format_size(option) == format_size(clothing_size):
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
                                if format_size(option) == format_size(clothing_size):
                                    return variant_id

                # If the item is footwear
                elif target_prod == 'footwear':
                    # If the item is found
                    if option == str(shoe_size):
                        return variant_id

                else:
                    print('Product type not found')

    print('\nProduct not found.')
    return None

# Returns product availability
def check_availability(prod_url, prod_id, var_id):

    domain = prod_url.split('/')[2].split('.')

    if len(domain) == 3:
        tld = domain[2]
    elif len(domain) == 2:
        tld = domain[1]

    web_json = prod_url.split(tld)[0] + tld + '/products.json?limit=1000'
    website = requests.get(web_json)
    products = json.loads((website.text))['products']

    # Checking availability
    for product in products:
        if product['id'] == prod_id:

            variants = product['variants']
            for variant in variants:

                if variant['id'] == var_id:
                    available = variant['available']

                    if available:
                        return True
    return False

# Creates and returns the cart url of item entered
def get_cart_link(prod_url, var_id):
    domain = prod_url.split('/')[2]
    cart_url = 'https://' + domain + '/cart/update?updates[' + str(var_id) + ']=1'
    return cart_url