
from bs4 import BeautifulSoup as bs
import requests
import time
import json

from utils import save_webpage


class Checkout:
    def __init__(self, cart_url, profile):
        self.session = requests.session()
        self.domain = cart_url.split("cart/")[0]
        self.cart_url = cart_url
        self.profile = profile
        self.pay_token = ""
        self.pay_gate = ""
        self.checkout = ""

    def load_payment(self):
        payload = {
            "credit_card": {
                "number": self.profile["Payment"]["Card Number"],
                "name": self.profile["Payment"]["Name"],
                "month": self.profile["Payment"]["Expiry Date (MM/YY)"].split("/")[0].strip(),
                "year": self.profile["Payment"]["Expiry Date (MM/YY)"].split("/")[1].strip(),
                "verification_value": self.profile["Payment"]["CVV"]
            }
        }

        payment = "https://elb.deposit.shopifycs.com/sessions"
        pay = requests.post(payment, json=payload, verify=False)

        if pay.status_code == requests.codes.ok:
            print("\nPayment authentication token successful.")
        else:
            print("\nPayment authentication token failed.")

        self.pay_token = json.loads(pay.text)["id"]

    def add_to_cart(self):
        print(self.cart_url)
        self.session.get("http://" + self.cart_url)
        cart = self.session.get("http://" + self.cart_url)
        self.checkout = cart.url

    def enter_personal(self):
        payload = {
            "_method": "patch",
            "authenticity_token": "",
            "previous_step": "contact_information",
            "step": "shipping_method",
            "checkout[email]": self.profile["Email"],
            "checkout[buyer_accepts_marketing]": "0",
            "checkout[buyer_accepts_marketing]": "1",
            "checkout[shipping_address][first_name]": self.profile["First Name"],
            "checkout[shipping_address][last_name]": self.profile["Last Name"],
            "checkout[shipping_address][address1]": self.profile["Address"],
            "checkout[shipping_address][address2]": self.profile["Address 2 (optional)"],
            "checkout[shipping_address][city]": self.profile["City"],
            "checkout[shipping_address][country]": self.profile["Country"],
            "checkout[shipping_address][province]": self.profile["Province"],
            "checkout[shipping_address][zip]": self.profile["Postal Code"],
            "checkout[shipping_address][phone]": self.profile["Phone Number"],
            "checkout[client_details][browser_width]": "1440",
            "checkout[client_details][browser_height]": "721",
            "checkout[client_details][javascript_enabled]": "1",
            "checkout[client_details][color_depth]": "30",
            "checkout[client_details][java_enabled]": "true",
            "checkout[client_details][browser_tz]": "240",
            "checkout[remember_me]": "0",
            "button": ""
        }

        r = self.session.post(f"{self.checkout}", data=payload)
        print("\nPersonal info - success.") if r.status_code == requests.codes.ok else print(
            "\nPersonal info - failed.")

    def get_shipping(self):
        postal_code = self.profile["Postal Code"]
        province = self.profile["Province"]
        country = self.profile["Country"]
        shipping = f"https://{self.domain}/cart/shipping_rates.json?shipping_address[zip]={postal_code}&shipping_address[country]={country}&shipping_address[province]={province}"
        r = self.session.get(shipping, verify=False)

        if r.status_code == requests.codes.ok:
            try:
                shipping_options = json.loads(r.text)
                ship_opt = shipping_options["shipping_rates"][0]["name"].replace(
                    " ", "%20")
                ship_rate = shipping_options["shipping_rates"][0]["price"]
                option = f"shopify-{ship_opt}-{ship_rate}"
                ship = {
                    "_method": "patch",
                    "authenticity_token": "",
                    "previous_step": "shipping_method",
                    "step": "payment_method",
                    "checkout[shipping_rate][id]": option,
                    "button": "",
                    "checkout[client_details][browser_width]": "1440",
                    "checkout[client_details][browser_height]": "721",
                    "checkout[client_details][javascript_enabled]": "1"
                }

                r = self.session.post(self.checkout, data=ship)
                print("\nShipping info filled successfully.") if r.status_code == requests.codes.ok else print(
                    "\nShipping info - failed.")

                try:
                    soup = bs(r.text, "lxml")
                    self.pay_gate = soup.find(
                        "input", {"name": "checkout[payment_gateway]"})["value"]
                    print("\nPayment Gate ID retreived")
                except Exception as e:
                    print(f"\nFailed to get the payment gateway token.\n{e}")

            except IndexError:
                print("\nFailed to retrieve shipping info - Personal info not filled.")

        else:
            print("\nFailed to load shipping page.")

    def pay(self):
        # Shopify CC Testing
        # Declined message - 4000000000000002
        # Incorrect number - 4242424242424241
        # Disputed transaction - 4000000000000259
        # Invalid Expiry Month - 12 < XX
        # Invalid Expiry Year - past year
        # Invalid CVV - any 2 digits

        payload = {
            "_method": "patch",
            "authenticity_token": "",
            "previous_step": "payment_method",
            "step": "",
            "s": self.pay_token,
            "checkout[payment_gateway]": self.pay_gate,
            "checkout[credit_card][vault]": "false",
            "checkout[different_billing_address]": "false",
            "complete": "1",
            "checkout[client_details][browser_width]": "1440",
            "checkout[client_details][browser_height]": "721",
            "checkout[client_details][javascript_enabled]": "1",
            "g-recaptcha-repsonse": "",
            "button": ""
        }

        r = self.session.post(
            self.checkout + "?step=payment_method", data=payload)

        if b"Check your card" in r.content:
            print("\nCard information is invalid - Checkout failed.")

        if r.status_code == requests.codes.ok:
            print("\nCheckout complete.")

    def checkout_prod(self):
        print("\nCheckout initiated.")
        start = time.time()
        self.load_payment()
        self.add_to_cart()
        self.enter_personal()
        self.get_shipping()
        self.pay()
        print("\nElapsed Time: %.2fs." % (time.time() - start))
