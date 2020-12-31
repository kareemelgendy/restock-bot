
import json, requests
import webbrowser

# Returns product's json data
def get_product(prod_url):

    try:
        # If a variant is in the url
        if len(prod_url.split('?')) > 1:
            prod_url = prod_url.split('?')[0]

        prod_json = prod_url.strip() + '.json'
        r = requests.get(prod_json)
        products = json.loads((r.text))
        return products
    
    except:
        return None

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

    size = size.replace('-', '').lower()

    # list of sizes and possibilities (x & xs)
    xxs = ['xxs', 'xxsm', 'xxsmall', '2xs']
    xs = ['xs', 'xsm', 'xsmall']
    xl = ['xl', 'xlg', 'xlarge']
    xxl = ['xxl', 'xxlg', 'xxlarge', '2xl']

    # Converting to recognizable size
    if size[0] == 'x' or size[0] == '2':
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

# Returns the product type
def get_prod_type(size):
    
    # Footwear w/ half sizes
    if '.' in size:
        try:
            float(size)
            prod_type = 'footwear'
        except ValueError:
            prod_type = 'clothing'
    
    # Footwear w/ whole sizes
    else:
        try:
            int(size)
            prod_type = 'footwear'
        except ValueError:
            prod_type = 'clothing'

    return prod_type

# Sets target action of product (Notification or Checkout)
def get_target(profile_dict, product_dict, title, line):

    current = line.replace('\n', '').split('|')

    # If entry is a number
    try:
        target = int(current[1].replace('-', '').strip())
        product_dict.set_val(title, 'Notification', target) ##########
        return True

    except ValueError:
        target = current[1].strip()

        if profile_dict.get_profile(target):
            product_dict.set_val(title, 'Profile', target)
            return True
        else:
            print('\n{} Could not retrieve product from (Invalid Profile Name/Number): \n{}'.format('\U0001f534', line))
            product_dict.remove_product(title)
            return False

# Gets the product's variant ID 
def get_variant_id(variants, target_prod, size, colour):
    
    # Checking variants
    for variant in variants:
        for i in range(1, 4):

            option = variant['option' + str(i)] 
            variant_id = variant['id'] 

            # If product has variants
            if option != None:
                option = option.lower()

                # Accessory
                if target_prod == 'accessory':
                    if option == 'default title' or option == 'o\/s':
                        print(variant_id)
                        return variant_id
                
                # Clothing
                elif target_prod == 'clothing':

                    # one variant - size
                    if colour == None: 
                        # Size is found
                        if format_size(option) == format_size(size):
                            return variant_id

                    # two variants - size & colour
                    else: 
                        # Size is found first 
                        if format_size(option) == format_size(size):
                            # Find colour in the current size
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]
                                if option == colour:
                                    return variant_id              
                        
                        # Colour is found first
                        elif option.lower() == colour.lower(): 
                            # Find size in the current colour
                            for i in range(i + 1, 3):
                                option = variant['option' + str(i)]
                                if format_size(option) == format_size(size):
                                    return variant_id

                # Footwear
                elif target_prod == 'footwear':
                    # If the item is found
                    if option == str(size):
                        return variant_id
                else:
                    print('Product type not supported.')
    
    print('Could not get variant ID')
    return None

# Returns product availability
def check_availability(prod_url, prod_id, var_id):

    url = prod_url.split('/products/')[0]
    web_json = '{}/products.json?limit=5000'.format(url)
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
                    else:
                        return False

    return 'Invalid'

# Creates and returns the cart url 
def generate_cart_link(prod_url, variant_id):
    domain = prod_url.split('/')[2]
    cart_url = 'https://{}/cart/update?updates[{}]=1'.format(domain, variant_id)
    return cart_url

# Processes product - Cart, Watch, or Ignore
def process_prod(product_dict, title, cart_url, availability, line):

    if availability == True:
        print('\n{} {} was found in stock - adding to cart'.format('\U0001f6d2', title))
        open_cart(cart_url)

        if product_dict.get_prod(title):
            product_dict.remove_product(title)

    elif not availability:
        print('\n{} {} added to watchlist'.format('\u2705', title)) 

    else:
        print('\n{} The following website is not currently supported OR invalid URL (make sure collection included)\n{}'.format('\U0001f534', line))
        product_dict.remove_product(title)

# Opens cart if product is available
def open_cart(cart_url):

    try:
        webbrowser.open(cart_url)
        return True
    except:
        #print('\nMake sure you have chromedriver installed and in restockBot folder.')
        #print('More information provided in the README file')
        print('Error occured could not open browser.')