import sys
import time
from checkout import Checkout
from notify.sms import notify_user

class WatchProcess:
    """
    Handles the watch process
    @param profiles: list of saved profiles
    @param products: list of saved products
    """
    def __init__(self, profiles, products):
        self.profiles = profiles
        self.products = products


    # Returns profile if valid
    def get_profile(self, name):
        for profile in self.profiles:
            if profile.get_name() == name:
                return profile
        return None


    # Removes in stock products
    def remove_in_stock(self) -> None:
        # Check each products availability
        for product in list(self.products):
            name = product.get_info()[0]
            if product.is_available():
                product.open_in_browser()
                print(f'\U0001F6D2 {name} in stock, opening in browser.')
                self.products.remove(product)

            time.sleep(1)
        # No products to watch
        if len(self.products) == 0:
            print('\U0001F64C All products were in stock.')
            sys.exit(0)

    # Commences watch process
    def begin(self) -> None:
        print('\n\U0001F680 Beginning watch process')
        self.remove_in_stock()

        while self.products:
            for product in list(self.products):
                name, vid, cart, profile_name, phone = product.get_info()
                profile = None

                # Get product availability
                if product.is_available():
                    # Checkout using profile
                    if profile_name:
                        profile = self.get_profile(profile_name)
                        if profile:
                            domain = cart.split('/cart')[0]
                            checkout = Checkout(vid, domain, profile)
                            checkout.run()
                        else:
                            print(f'\U0001F6D1 Profile with the name {profile_name} was not found.')
                            print(f'Product available here: {cart}')

                    # Send an SMS
                    elif phone:
                        msg = f'\U0001F6CD {name} is back in stock. Checkout here: {cart}'
                        notify_user(phone, msg)

                    # Remove once done
                    self.products.remove(product)

                else:
                    print(f'\U0001F440 {name} is still out of stock :/')

                # Cooldown
                time.sleep(10)

        print('\U0001F44B No more products in watchlist.')
