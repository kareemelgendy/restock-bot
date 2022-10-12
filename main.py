import sys
from profile import Profile
from product import Product
from watch import WatchProcess
from helpers import read_data


def main():
    # Reading data from profile and product files
    profiles_file = read_data('profiless')
    products_file = read_data('productss')
    products, profiles = [], []

    # Creating list of Profiles and Products
    for name, profile in profiles_file.items():
        if profile['Email']:
            profiles.append(Profile(name, profile))

    for product in products_file:
        if product['Product URL']:
            products.append(Product(product))

    # Begin watch process
    if products:
        watch_process = WatchProcess(profiles, products)
        watch_process.begin()
    else:
        print('No products found.')
        print('Enter products in data/products.json')
        print('Refer to README.md for instructions')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n\U0001F44B Ending watch process...')
        sys.exit(0)
