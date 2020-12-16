
# Function that checks if the user entered a valid shoe size
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

# Function that gets the product type and its required options
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

# Function that gets the number of items the user wants to cart
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

# Function that gets check if the user would like to retry if a mistake is made 
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

def getAutoCheckout(product_name, product_id, variant_id):
    print('\nWould you like to attempt to check it out automatically')
    auto_checkout = input('when the product becomes available? (y/n): ')

    if auto_checkout == 'y':

        prod_dict = Product()
        prod_dict.newProduct(product_name, product_id, variant_id)

        print('Add info to file') 
        getUserInfo()
        # return profil dict

    elif auto_checkout == 'n':
        print('Make sure to check back later!') ##### update user in another way
        print('Quitting now...')
        quit() 
    else:
        getAutoCheckout(product_name, product_id, variant_id)

def getWatchOption(profile_dict, product_dict, product_name, product_id, variant_id):
    watch_prod = input('Would you like to watch this product? (y/n): ')

    if watch_prod == 'y':
        print('\nAdding product to watch the list...') ###### Add product to watchlist - product dictionary
        getAutoCheckout(product_name, product_id, variant_id)
        
    elif watch_prod == 'n':
        if len(profile_dict) == 0:
            print('\nQuitting now...')
            quit()
        else:
            print('Press X to call the program menu') ###
    else:
        getWatchOption(product_name, product_id, variant_id)