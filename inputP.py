
# Function that checks if the user entered a valid shoe size
def getShoeSize():
    try:
        shoe_size = float(input('\nEnter Shoe Size: ')).lower()

        if shoe_size % 1 == 0 or shoe_size % 1 == 0.5:
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
    print("Enter one of the following ('clothing', 'footwear', or 'item')")
    target_type = input('Enter Product Type (q to quit): ').lower()

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
        print("Invalid input - please enter a valid whole number.")
        getCartNum()

# Function that gets check if the user would like to retry if a mistake is made 
def retryEntry(target_product_id):
    
    if target_product_id == None:
        print('Make sure to enter a valid/live product url and enter correct options')
        retry = input('Would you like to try again? (y/n): ')

        if retry == 'y':
            return True

        elif retry == 'n':
            return False

        else:
            retryEntry()

    else:
        getCartNum()

# Function that gets product confirmation from the user
def getConf():

    confirmation = input('Is the product above correct (y/n): ')

    if confirmation == 'y':
        return True

    elif confirmation == 'n':
        return False

    # Invalid input
    else:
        print('\nInvalid input, please try again')
        getConf()
