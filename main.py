
from inputP import getProdType, getCartNum, retryEntry
from utilitiesP import loadProd, getNumVariants, getProdId
from outputP import sendConf

print('----------------------------------------------------------')
print('                  Welcome to RestockBot')
print('----------------------------------------------------------')
print('Product types supported (clothing, footwear, accessories):')
print('-Clothing items with letter sizing and/or colour options')
print('-Accessories with no variants (one option)')
print('-Footwear with number size options')
print('----------------------------------------------------------')

# Getting the url from the user
prod_url = input('\nInsert Product URL: ')

prod_title = loadProd(prod_url)[0]
variants = loadProd(prod_url)[1]

num_variants = getNumVariants(variants)
target_type = getProdType()
target_product_id = getProdId(variants, target_type)
num_items = getCartNum()

sendConf(prod_url, prod_title, num_variants, target_product_id, num_items, target_type)
