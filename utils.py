from typing import Tuple, Union
import webbrowser
import requests
import json


def fetch_data(file: str) -> dict:
    try:
        with open(f'data/{file}.json') as f:
            data = json.load(f)
        f.close()

        return data
    except:
        print("File not found.")


def write_to_file(file: str, data: dict) -> None:
    try:
        with open(f'data/{file}.json', "w") as f:
            json.dump(data, f, indent=2)
        f.close()
    except:
        print("Failed to save dict in JSON file.")


def formatSize(size: str) -> str:
    size = size.replace("-", "").lower()
    return size[0:2] if size[0] == "x" else size[0]


def gen_cart_url(prod_url: str, vid: int) -> str:
    url = prod_url.split("/")
    for x in url:
        if "." in x:
            domain = x

    cart_url = f'https://{domain}/cart/{vid}:1'
    return cart_url


def get_product(prod_url: str, size: Union[str, int]) -> Tuple[str]:
    r = requests.get(prod_url + ".json")
    product = json.loads(r.text)["product"]

    pid = product["id"]
    name = f'{product["title"]} {"- " + size if size else ""}'
    variants = product["variants"]

    for variant in variants:
        if formatSize(variant["title"]) == formatSize(size):
            vid = variant["id"]

    return name, pid, vid


def fetch_prod_details(products: dict) -> dict:
    for name, details in list(products.items()):
        url, size = details["Product URL"], details["Size"]
        new, pid, vid = get_product(url, size)
        cart_url = gen_cart_url(url, vid)

        details["Product ID"] = pid
        details["Variant ID"] = vid
        details["Cart URL"] = cart_url
        products[new] = products.pop(name)

    with open("data/products.json", "w") as f:
        json.dump(products, f, indent=2)
    f.close()

    return products


def check_availability(pid: int, vid: int, cart_url: str) -> bool:
    catalog = f"https://{cart_url.split('cart/')[0]}/products.json?limit=5000"
    r = requests.get(catalog)
    products = json.loads(r.text)["products"]

    for product in products:
        if product["id"] == pid:
            variants = product['variants']
            for variant in variants:
                if variant['id'] == vid:
                    return variant["available"]
    return False


def open_cart(cart_url: str) -> None:
    try:
        webbrowser.open(cart_url)
    except:
        print("\nError occurred could not open cart in browser.")
