
from notify import notify_user

# Validates user entry for shoe size
def get_shoe_size():
    
    try:
        shoe_size = float(input('\nEnter Shoe Size: '))
        if shoe_size % 1 == 0 or shoe_size % 1 == 0.5:
            if shoe_size % 1 ==  0:
                shoe_size = int(shoe_size)
            return shoe_size
        else:
            print("Invalid input - please enter a valid number.")
            get_shoe_size()

    except ValueError:
        print("Invalid input - please enter a valid shoe size.")
        get_shoe_size()

    else:
        return None

# Returns the product type and its options
def get_prod_type():
    # Get the product type
    print("\nEnter one of the following ('clothing', 'footwear', or 'item')")
    target_type = input('Enter Product Type (q anytime to quit): ').lower()

    # Checking the product type 
    if target_type == 'clothing':
        clothing_size = input('\nEnter Clothing Size: ').lower()
        clothing_colour = input('\nEnter Colour: ').lower()
        return target_type, clothing_size, clothing_colour
    elif target_type == 'footwear':
        size = get_shoe_size()
        return target_type, size
    elif target_type == 'item':
        return target_type
    elif target_type == 'q':
        quit()
    else:
        print('\nInvalid input - please try again')
        get_prod_type()

    return None

# Creates a new profile
def create_profile(profile_dict, product_dict, product_name):
    profile_name = input('\nProfile Name: ')
    profile_dict.new_profile(profile_name)

    profile_dict.set_val(profile_name, 'First Name', input('First Name: '))
    profile_dict.set_val(profile_name, 'Last Name', input('Last Name: '))
    profile_dict.set_val(profile_name, 'Email', input('Email: '))
    profile_dict.set_val(profile_name, 'Address', input('Address 1: '))
    profile_dict.set_val(profile_name, 'Address 2', input('Address 2 (optional): '))

    profile_dict.set_val(profile_name, 'Country', input('Country: '))
    profile_dict.set_val(profile_name, 'Province', input('Province/State: '))
    profile_dict.set_val(profile_name, 'City', input('City: '))
    profile_dict.set_val(profile_name, 'Postal Code', input('Postal Code: '))
    profile_dict.set_val(profile_name, 'Phone', input('Phone Number: ').strip(' -'))

    profile_dict.set_val(profile_name, 'CC Number', input('Credit Card Number: ').strip(' '))
    profile_dict.set_val(profile_name, 'CC Name', input('Name on CC: '))
    profile_dict.set_val(profile_name, 'Expiry', input('Expiry (MM/YY): '))
    profile_dict.set_val(profile_name, 'CVV', input('CVV: '))

    # Assigning profile to use for product checkout
    if product_dict != None:
        product_dict.set_val(product_name, 'Profile', profile_name)

# Auto checkout preference
def get_auto_checkout(profile_dict, product_dict):

    print('\nWould you like to attempt to check it out automatically')
    auto_checkout = input('when the product becomes available? (y/n): ')

    if auto_checkout == 'y':
        if(profile_dict.is_empty()):
            print('\nCreate your profile below: ')
            print('Enter required fields correctly. Press enter to skip fields that do not apply.')
            return True
        else:
            pass

    elif auto_checkout == 'n':

        if product_dict.is_empty():
            print('Make sure to check back later!') ##### update user in another way
            print('Quitting now...')
            quit() 

    else:
        get_auto_checkout(profile_dict, product_dict)

# Product watch preference
def get_watch_option():
    watch_prod = input('\nWould you like to watch this product? (y/n): ')

    if watch_prod == 'y':
        return True
        
    elif watch_prod == 'n':
        if profile_dict.is_empty():
            print('\nQuitting now...')
            quit()
        else:
            pass
    else:
        get_watch_option()

# Adding another product
def get_new_prod(prod_dict):
    
    new_prod = input('\nWould you like to enter another product? (y/n): ')

    if new_prod == 'y':
        return True

    elif new_prod == 'n':
        if prod_dict.is_empty():
            print('Watchlist is empty - quitting now')
            quit()

    else:
        get_new_prod(prod_dict)
