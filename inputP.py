
from profileDict import Profile
from productDict import Product

# Validates user entry for shoe size
def getShoeSize():
    try:
        shoe_size = float(input('\nEnter Shoe Size: '))
        if shoe_size % 1 == 0 or shoe_size % 1 == 0.5:
            if shoe_size % 1 ==  0:
                shoe_size = int(shoe_size)
            return shoe_size
        else:
            print("Invalid input - please enter a valid number.")
            getShoeSize()

    except ValueError:
        print("Invalid input - please enter a valid shoe size.")
        getShoeSize()
    else:
        return None

# Returns the product type and its options
def getProdType():
    # Get the product type
    print("\nEnter one of the following ('clothing', 'footwear', or 'item')")
    target_type = input('Enter Product Type (q anytime to quit): ').lower()

    # Checking the product type 
    if target_type == 'clothing':
        clothing_size = input('\nEnter Clothing Size: ').lower()
        clothing_colour = input('\nEnter Colour: ').lower()
        return target_type, clothing_size, clothing_colour
    elif target_type == 'footwear':
        size = getShoeSize()
        return target_type, size
    elif target_type == 'item':
        return target_type
    elif target_type == 'q':
        quit()
    else:
        print('\nInvalid input - please try again')
        getProdType()

    return None

# Gets the number of items the user wants to cart
def getCartNum():
    print('\nHow many would you like to cart?')

    try:
        num_items = int(input('Enter number (1 recommended for products with high demand): '))
        return num_items
    except ValueError:
        if num_items == 'q':
            quit()
        else:
            print("Invalid input - please enter a valid whole number.")
            getCartNum()

# Catches mistakes and reruns program
def retryEntry(target_product_id):
    
    if target_product_id == None:
        print('\nMake sure you enter a valid/live product url and the correct options.')
        retry = input('Would you like to try again? (y/n): ')
        if retry == 'y':
            return True ##### run the program again
        elif retry == 'n':
            quit()
        else:
            retryEntry()
    else:
        print('Error - Invalid entry (size or colour')


def getUserInfo(profile_dict, product_dict, product_name):

    if(len(profile_dict) == 0):
        print('\nCreate your profile below: ')
        createProfile(profile_dict, product_dict, product_name)
    else:
        print('\nWhich profile would you like to use: ') #####
        print('list all profiles here.')

# Creates a new profile
def createProfile(profile_dict, product_dict, product_name):
    profile_name = input('\nProfile Name: ')
    profile_dict.newProfile(profile_name)

    profile_dict.setVal(profile_name, 'First Name', input('First Name: '))
    profile_dict.setVal(profile_name, 'Last Name', input('Last Name: '))
    profile_dict.setVal(profile_name, 'Email', input('Email: '))
    profile_dict.setVal(profile_name, 'Address', input('Address 1: '))
    profile_dict.setVal(profile_name, 'Address 2', input('Address 2 (optional): '))

    country = input('Country: ')
    profile_dict.setVal(profile_name, 'Country', country)

    if country[0].lower() == 'u':
        profile_dict.setVal(profile_name, 'State', input('State: '))
    elif country[0].lower() == 'c':
        profile_dict.setVal(profile_name, 'Province', input('Province: '))

    profile_dict.setVal(profile_name, 'City', input('City: '))
    profile_dict.setVal(profile_name, 'Postal Code', input('Postal Code: '))
    profile_dict.setVal(profile_name, 'Phone', input('Phone Number: ').strip(' -'))

    profile_dict.setVal(profile_name, 'CC Number', input('Credit Card Number: ').strip(' '))
    profile_dict.setVal(profile_name, 'CC Name', input('Name on CC: '))
    profile_dict.setVal(profile_name, 'Expiry Month', input('Expiry Month (2 Digits): '))
    profile_dict.setVal(profile_name, 'Expiry Year', input('Expiry Year (4 Digits): '))
    profile_dict.setVal(profile_name, 'CVV', input('CVV: '))

    # Assigning profile to use for product checkout
    product_dict.setVal(product_name, 'Profile', profile_name)

# Checks if the user would like to automatically check out the item
def getAutoCheckout(profile_dict, product_dict, product_name):

    # profile_dict, product_dict, product_name, product_id, variant_id

    print('\nWould you like to attempt to check it out automatically')
    auto_checkout = input('when the product becomes available? (y/n): ')

    if auto_checkout == 'y':
        print(str(profile_dict.size()))
        if(profile_dict.size() == 0):
            print('\nCreate your profile below: ')
            print('Enter required fields correctly. Press enter to skip fields that do not apply.')
            createProfile(profile_dict, product_dict, product_name)

            #watchProducts(profile_dict, product_dict)
        else:
            print('\nWhich profile would you like to use: ') #####
            print('list all profiles here.') ######

    elif auto_checkout == 'n':
        print('Make sure to check back later!') ##### update user in another way
        print('Quitting now...')
        quit() 
    else:
        getAutoCheckout(profile_dict, product_dict, product_name)

# Checks if the user wants to watch the entered product
def getWatchOption(profile_dict, product_dict, product_name, product_id, variant_id, cart_url):
    watch_prod = input('Would you like to watch this product? (y/n): ')

    if watch_prod == 'y':
        # num_items = getCartNum() ###
        
        product_dict.newProduct(product_name) ## Adding product to watchlist
        product_dict.setVal(product_name, 'Product ID', product_id)
        product_dict.setVal(product_name, 'Variant ID', variant_id)
        product_dict.setVal(product_name, 'Cart URL', cart_url)

        getAutoCheckout(profile_dict, product_dict, product_name)
        
    elif watch_prod == 'n':
        if profile_dict.size() == 0:
            print('\nQuitting now...')
            quit()
        else:
            print('Press X to call the program menu') ###
    else:
        getWatchOption(product_name, product_id, variant_id)