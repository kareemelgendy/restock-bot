
from product_dict import Product
from profile_dict import Profile
from watch import watch_products
from file_reader import *

import time

# Supported products 
print('''\
\n{}\n\t\t{} Welcome to RestockBot\n{}
Product types supported:
{} Clothing items with letter sizing (xxs - xxl) and/or colour options
{} Footwear with number size options (whole & half sizes)
{} Accessories with no variants (o/s - one option)
* Note * This is a generic script and does not support all Shopify stores.
'''.format('-' * 58, '\U0001F916', '-' * 58, '\U0001f455', '\U0001f45f', '\U0001f392'))

# Instructions on running the script
print('''\
To get started:
1. Insert products in products.txt (with all parameters filled)
2. Insert profiles in profiles.txt (For automatic checkout of sold out items)
3. Rerun script (if products/profiles files currently empty)
{}
'''.format('-' * 58))

# Dictionary initialization
profiles = Profile()
products = Product()

time.sleep(2)

# Getting Profiles & Products from txt files
get_profiles(profiles)
get_products(profiles, products)

watch = False

# Product Watchlist
if not products.is_empty():
    watch = True
    watch_products(profiles, products)

# Watch process never initiated
if not watch:
    print('\n{} No products being watched. Quitting now...'.format('\U0001F44B'))
    quit()
