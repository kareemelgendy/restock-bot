from utils import check_availability, open_cart, write_to_file
from notify.twilio import notify_user
from checkout import Checkout
import time


# Too many requests to the same website in a short period will flag you
def watch_prods(profiles: dict, products: dict) -> None:
    in_stock = {}

    print("\nChecking products...")
    for name, details in list(products.items()):
        pid, vid, cart_url = details["Product ID"], details["Variant ID"], details["Cart URL"]
        available = check_availability(pid, vid, cart_url)

        if available:
            open_cart(cart_url)
            print(f'{name} in stock, opening in browser.')
            in_stock[name] = products.pop(name)

        # time.sleep()

    write_to_file("in-stock", in_stock)
    write_to_file("products", products)
    print("\nBeginning the watch process.")
    watch = True

    while products:
        for name, details in list(products.items()):
            pid, vid, cart_url = details["Product ID"], details["Variant ID"], details["Cart URL"]
            available = check_availability(pid, vid, cart_url)

            if available and watch:
                if details["Profile"]:
                    try:
                        checkout = Checkout(
                            cart_url, profiles[details["Profile"]])
                        checkout.checkout_prod()
                    except:
                        print(
                            "\nCheckout unsuccessful - webpage saved for reference.")

                elif details["Notification"]:
                    try:
                        msg = f'{name} is back in stock. Checkout here: {cart_url}'
                        notify_user(details["Notification"], msg)
                    except:
                        print("\nFailed to send a text message.")

                else:
                    print(f"{name} is back in stock - check out here: {cart_url}")
                    open_cart(cart_url)

                in_stock[name] = products.pop(name)
                write_to_file("in-stock", in_stock)
                write_to_file("products", products)

            else:
                print(f'{name} -- Out of Stock.')

        time.sleep(10)
