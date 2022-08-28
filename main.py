from watch import watch_prods
from utils import fetch_data, fetch_prod_details

profiles = fetch_data("profiles")
products = fetch_data("products")

if products:
    products = fetch_prod_details(products)
    watch_prods(profiles, products)
else:
    print("\nNo products found.")
    print("Enter products in data/products.json")
    print("Refer to README.md for instructions")
    quit()
