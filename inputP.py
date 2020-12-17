
from profileDict import Profile
from productDict import Product

# getShoeSize, getProdType, getUserInfo, createProfile, getAutoCheckout, getWatchOption

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
    
#     if target_product_id == None:
#         print('\nMake sure you enter a valid/live product url and the correct options.')
#         retry = input('Would you like to try again? (y/n): ')
#         if retry == 'y':
#             return True ##### run the program again
#         elif retry == 'n':
#             quit()
#         else:
#             retryEntry()
#     else:
#         print('Error - Invalid entry (size or colour')


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

    profile_dict.setVal(profile_name, 'Country', input('Country: '))
    profile_dict.setVal(profile_name, 'Province', input('Province/State: '))
    profile_dict.setVal(profile_name, 'City', input('City: '))
    profile_dict.setVal(profile_name, 'Postal Code', input('Postal Code: '))
    profile_dict.setVal(profile_name, 'Phone', input('Phone Number: ').strip(' -'))

    profile_dict.setVal(profile_name, 'CC Number', input('Credit Card Number: ').strip(' '))
    profile_dict.setVal(profile_name, 'CC Name', input('Name on CC: '))
    profile_dict.setVal(profile_name, 'Expiry', input('Expiry (MM/YY): '))
    profile_dict.setVal(profile_name, 'CVV', input('CVV: '))

    # Assigning profile to use for product checkout
    product_dict.setVal(product_name, 'Profile', profile_name)

# Checks if the user would like to automatically check out the item
def getAutoCheckout(profile_dict):

    # profile_dict, product_dict, product_name, product_id, variant_id

    print('\nWould you like to attempt to check it out automatically')
    auto_checkout = input('when the product becomes available? (y/n): ')

    if auto_checkout == 'y':
        if(profile_dict.size() == 0):
            print('\nCreate your profile below: ')
            print('Enter required fields correctly. Press enter to skip fields that do not apply.')
            return True

        else:
            print('\nWhich profile would you like to use: ') #####
            print('list all profiles here.') ######

    elif auto_checkout == 'n':
        print('Make sure to check back later!') ##### update user in another way
        print('Quitting now...')
        quit() 
    else:
        getAutoCheckout()

# Checks if the user wants to watch the entered product
def getWatchOption():
    watch_prod = input('Would you like to watch this product? (y/n): ')

    if watch_prod == 'y':
        return True
        
    elif watch_prod == 'n':
        if profile_dict.size() == 0:
            print('\nQuitting now...')
            quit()
        else:
            print('Press X to call the program menu') #### Command to call menu to modify/termiante the program
    else:
        getWatchOption()

def getNewProd(prod_dict):
    
    newProd = input('Would you like to enter another product? (y/n): ')

    if newProd == 'y':
        return True

    elif newProd == 'n':
        if prod_dict.size() == 0:
            print('Watchlist is empty - quitting now')
            quit()

    else:
        getNewProd()