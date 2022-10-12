import time
import json
import requests
from bs4 import BeautifulSoup as bs


class Checkout:
    """
    Checkout process
    @param vid: the product variant id
    @param domain: the website selling the product
    @param profile: the profile to use at checkout
    """
    def __init__(self, vid, domain, profile):
        self.session = requests.session()
        self.vid = vid
        self.domain = domain
        self.profile = profile
        self.pay_token = ''
        self.pay_gate = ''
        self.checkout = ''


    # Gets payment authentication token
    def load_payment(self) -> None:
        payload = {
            'credit_card': {
                'number': self.profile.get_cc()['Card Number'],
                'name': self.profile.get_cc()['Name'],
                'month': self.profile.get_cc()['Expiry Date (MM/YY)'].split('/')[0].strip(),
                'year': self.profile.get_cc()['Expiry Date (MM/YY)'].split('/')[1].strip(),
                'verification_value': self.profile.get_cc()['CVV']
            }
        }
        payment = 'https://elb.deposit.shopifycs.com/sessions'
        pay = requests.post(payment, json=payload, verify=False)
        if pay.status_code == 200:
            print('Payment authentication token successful.')
        else:
            print('Payment authentication token failed.')

        self.pay_token = json.loads(pay.text)['id']


    # Adds the product to the cart
    def add_to_cart(self) -> None:
        self.session.get(f'{self.domain}/cart/add.js?id={self.vid}')
        cart = self.session.get(f'{self.domain}/checkout')
        self.checkout = cart.url


    # Enters personal information on the first page
    def enter_personal(self) -> None:
        payload = {
            '_method': 'patch',
            'authenticity_token': '',
            'previous_step': 'contact_information',
            'step': 'shipping_method',
            'checkout[email]': self.profile.get_email(),
            'checkout[buyer_accepts_marketing]': '1',
            'checkout[shipping_address][first_name]': self.profile.get_first_name(),
            'checkout[shipping_address][last_name]': self.profile.get_last_name(),
            'checkout[shipping_address][address1]': self.profile.get_address(),
            'checkout[shipping_address][address2]': self.profile.get_address2(),
            'checkout[shipping_address][city]': self.profile.get_city(),
            'checkout[shipping_address][country]': self.profile.get_country(),
            'checkout[shipping_address][province]': self.profile.get_province(),
            'checkout[shipping_address][zip]': self.profile.get_postal(),
            'checkout[shipping_address][phone]': self.profile.get_phone(),
            'checkout[client_details][browser_width]': '1440',
            'checkout[client_details][browser_height]': '721',
            'checkout[client_details][javascript_enabled]': '1',
            'checkout[client_details][color_depth]': '30',
            'checkout[client_details][java_enabled]': 'true',
            'checkout[client_details][browser_tz]': '240',
            'checkout[remember_me]': '0',
            'button': ''
        }
        r = self.session.post(f'{self.checkout}', data=payload)
        if r.status_code == 200:
            print('Personal info - success.')
        else:
            print('Personal info - failed.')


    # Gets the cheapest/first shipping option
    def get_shipping(self) -> None:
        postal = self.profile.get_postal()
        province = self.profile.get_province()
        country = self.profile.get_country()
        shipping = f'{self.domain}/cart/shipping_rates.json?shipping_address[zip]={postal}&shipping_address[country]={country}&shipping_address[province]={province}'
        r = self.session.get(shipping, verify=False)

        if r.status_code == 200:
            try:
                options = json.loads(r.text)
                ship_opt = options['shipping_rates'][0]['name'].replace(
                    ' ' , '%20')
                ship_rate = options['shipping_rates'][0]['price']
                option = f'shopify-{ship_opt}-{ship_rate}'
                data = {
                    '_method': 'patch',
                    'authenticity_token': '',
                    'previous_step': 'shipping_method',
                    'step': 'payment_method',
                    'checkout[shipping_rate][id]': option,
                    'button': '',
                    'checkout[client_details][browser_width]': '1440',
                    'checkout[client_details][browser_height]': '721',
                    'checkout[client_details][javascript_enabled]': '1'
                }
                r = self.session.post(self.checkout, data=data)
                if r.status_code == 200:
                    print('Shipping info filled successfully.')
                else:
                    print('Shipping info - failed.')

            except IndexError:
                print('Failed to retrieve shipping info.')
        else:
            print('Failed to load shipping page.')


    # Gets payment gateway
    def gateway(self) -> None:
        r = self.session.get(f'{self.checkout}?step=payment_method')
        soup = bs(r.text, 'html.parser')
        self.pay_gate = soup.find(
            'input', {'name': 'checkout[payment_gateway]'})['value']
        if self.pay_gate:
            print('Payment Gate ID retreived')
        else: print('Failed to get the payment gateway token.')


    # Enters payment information on checkout page
    def pay(self) -> None:
        payload = {
            '_method': 'patch',
            'authenticity_token': '',
            'previous_step': 'payment_method',
            'step': '',
            's': self.pay_token,
            'checkout[payment_gateway]': self.pay_gate,
            'checkout[credit_card][vault]': 'false',
            'checkout[different_billing_address]': 'false',
            'complete': '1',
            'checkout[client_details][browser_width]': '1440',
            'checkout[client_details][browser_height]': '721',
            'checkout[client_details][javascript_enabled]': '1',
            'g-recaptcha-repsonse': '',
            'button': ''
        }
        r = self.session.post(
            self.checkout + '?step=payment_method', data=payload)

        if b'Check your card' in r.content:
            print('Card information is invalid - Checkout failed.')
        if r.status_code == 200:
            print('Checkout attempt complete.')
            print('Webpage saved for review @ result.html')

        with open('result.html', 'wb+') as f:
            f.write(r.content)


    # Runs entire checkout process
    def run(self) -> None:
        print('\nCheckout initiated.')
        start = time.time()
        self.load_payment()
        self.add_to_cart()
        self.enter_personal()
        self.get_shipping()
        self.gateway()
        self.pay()
        print(f'Elapsed Time: {round(time.time() - start, 2)}.')
