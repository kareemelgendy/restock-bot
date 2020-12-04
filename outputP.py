
from inputP import getConf
from utilitiesP import getProdType, formatSize

# Confirm the right product has been found
def sendConf(prod_url, prod_title, num_variants, prod_id, num_items, target_type):

    clothing_size = formatSize(target_type[1]).upper()
    clothing_colour = target_type[2]
    target_type = target_type[0]

    # If a product was found 
    if prod_id != None:

        # Printing product specifications
        print('\n---------------------------------')
        print('           Product Found')
        print('---------------------------------')
        print('Product Name: ' + str(prod_title))

        # Print the options 
        if target_type == 'clothing':
            if num_variants == 2:
                print('Product Size: ' + str(clothing_size))
                print('Product Colour: ' + str(clothing_colour).title())
            else:
                print('Product Size: ' + str(clothing_size))

        elif target_type == 'shoes':
            print('Product Size: ' + str(clothing_size).upper())

        print('Product ID: ' + str(prod_id))
        print('---------------------------------')

        # If the correct product was found
        if getConf():
            cart_url = prod_url.split('.com')[0] + '.com/cart/update?updates[' + str(prod_id) + ']=' + str(num_items)
            item_url = prod_url + '?variant=' + str(prod_id)
            print('Cart link: ' + (cart_url))
            print('Product page link: ' + (item_url))
            #driver = webdriver.Chrome('./chromedriver')
            #driver.get(item_url)

        # If the wrong product was found
        elif not getConf():
            print('Make sure to enter a valid/live product url and enter correct options')
            quit() #######

    # If no product was found
    else:
        print('Item not found')