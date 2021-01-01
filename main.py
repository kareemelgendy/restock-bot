
from product_dict import Product
from profile_dict import Profile
from watch import watch_products
from file_reader import *

import time

# To Do:
# Catch Duplicate products
# Implement proxy support
# Automate checkout
# Optimize process

# Instructions
print('\n' + ('-' * 58))
print('\t\tWelcome to RestockBot')
print('-' * 58)
print('Product types supported:')
print('{} Clothing items with letter sizing (xxs - xxl) and/or colour options'.format('\U0001f455'))
print('{} Footwear with number size options (whole & half sizes)'.format('\U0001f45f'))
print('{} Accessories with no variants (o/s - one option)'.format('\U0001f392'))
print('\nTo get started: ')
print('1. Insert product links in products.txt')
print('2. Insert profiles in profiles.txt (For automatic checkout)')
print('3. Rerun script (if products/profiles files currently empty)')
print('-' * 58)

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
