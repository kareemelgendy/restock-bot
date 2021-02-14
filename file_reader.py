
from utilities import *
from profile_dict import Profile

# Reads profiles from txt file
def get_profiles(profile_dict):

    try:
        with open('./txt/profiles.txt') as f:

            # Skipping instructions and examples
            for i in range(30):
                f.readline()

            profile_name = None 
            for line in f:
                current = line.split(':')
                if len(current) == 2:
                    # Profile key and value
                    key = current[0].strip()
                    value = current[1].strip()

                    # New profile
                    if key == 'Profile Name' and len(value) > 0:
                        profile_name = value.strip()
                        profile_dict.new_profile(profile_name)

                    # Valid entry
                    if profile_name and key.strip() and value.strip():
                        profile_dict.set_val(profile_name, key, value) 

        f.close()

        if not profile_dict.is_empty():
            print('\n{} Profiles imported from txt file.'.format('\U0001f4b3'))

    except FileNotFoundError:
        print('\nProfile file not found.')

# Reads products from txt file
def get_products(profile_dict, product_dict):

    try:
        with open('./txt/products.txt') as f:

            # Skipping Instructions and examples
            for i in range(27): 
                f.readline()

            for line in f:
                current = line.replace('\n', '').split('|')
                param = len(current)

                # If invalid number of parameters
                if '/' in line and ((param >= 1 and param < 2) or param > 4):
                    print('\n{} The following product could not be watched (Invalid number of parameters):\n{}'.format('\U0001f534', line))
                    
                else:
                    prod_url = current[0]
                    product_info = get_product(prod_url) 

                    # Product found
                    if product_info != None:

                        try:
                            # Product Information
                            title = product_info['product']['title'].title() 
                            pid = product_info['product']['id'] # Product ID
                            variants = product_info['product']['variants'] # Product variants
                            found = True
                        
                        except KeyError:
                            found = False  

                        if found:
                            num_variants = get_num_variants(product_info['product']['variants'])

                            if num_variants != None:
                                product_dict.new_product(title) # Adding product to watchlist    
                                product_dict.set_val(title, 'Product URL', prod_url)
                                product_dict.set_val(title, 'Product ID', pid)

                                # Notification or checkout
                                valid = get_target(profile_dict, product_dict, title, line)

                                # Accessory
                                if valid and param == 2 and num_variants == 1:
                                    vid = get_variant_id(variants, 'accessory', None, None)
                                    cart_url = generate_cart_link(prod_url, vid)
                                    product_dict.set_val(title, 'Variant ID', vid)
                                    product_dict.set_val(title, 'Cart URL', cart_url)

                                    availability = check_availability(prod_url, pid, vid)
                                    process_prod(product_dict, title, cart_url, availability, line)

                                # Clothing with 1 variant or footwear
                                elif valid and param == 3 and num_variants == 1:
                                    size = current[2].strip()
                                    prod_type = get_prod_type(size)

                                    vid = get_variant_id(variants, prod_type, size, None)
                                    cart_url = generate_cart_link(prod_url, vid)
                                    product_dict.set_val(title, 'Variant ID', vid)
                                    product_dict.set_val(title, 'Cart URL', cart_url)

                                    availability = check_availability(prod_url, pid, vid)
                                    process_prod(product_dict, title, cart_url, availability, line)

                                # Clothing with size and colour variants
                                elif valid and param == 4 and num_variants == 2:
                                    size = current[2].strip()
                                    colour = current[3].strip()

                                    vid = get_variant_id(variants, 'clothing', size, colour)
                                    cart_url = generate_cart_link(prod_url, vid)
                                    product_dict.set_val(title, 'Variant ID', vid)
                                    product_dict.set_val(title, 'Cart URL', cart_url)

                                    availability = check_availability(prod_url, pid, vid)
                                    process_prod(product_dict, title, cart_url, availability, line)

                                else:
                                    if param != None and valid:
                                        print('\n{} The following product could not be watched (Invalid number of parameters):\n{}'.format('\U0001f534', line))

                                        # If in dictionary and invalid 
                                        if product_dict.get_prod(title):
                                            product_dict.remove_product(title)
                            
                            else:
                                print('\n{} Could not retrieve product from (Variant count not supported): \n{}'.format('\U0001f534', line))      

                        # Invalid URL
                        else:
                            if line != '\n':
                                print('\n{} Could not retrieve product from (Invalid URL): \n{}'.format('\U0001f534', line))      
        f.close()

        if not product_dict.is_empty():
            print('\nProducts imported from products.txt.\n{} Watch process started.'.format('\U0001f440'))

    except FileNotFoundError:
        print('\nProducts file not found.')
