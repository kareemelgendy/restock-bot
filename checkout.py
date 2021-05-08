
import requests, json, time
from bs4 import BeautifulSoup as bs
import profile_dict

class shopify_checkout:

    # Constructor
    def __init__(self, cart_url, profile_name, profile_dict):
        self.session = requests.session()
        self.cart_url = cart_url
        self.profile_dict = profile_dict
        self.profile_name = profile_name
        self.domain = cart_url.split('/')[2]

        self.checkout = ''
        self.pay_token = ''
        self.pay_gate = ''

    # Loads payment and retrieves payment token
    def load_payment(self):

        # Form Data - call cc info 
        payload = {
            'credit_card': {
                'number': self.profile_dict.get_val(profile_name, 'CC Number'),
                'name': self.profile_dict.get_val(profile_name, 'CC Name'),
                'month': self.profile_dict.get_val(profile_name, 'CC Expiry Date (MM/YY)').split('/')[0].strip(),
                'year': self.profile_dict.get_val(profile_name, 'CC Expiry Date (MM/YY)').split('/')[0].strip(),
                'verification_value': self.profile_dict.get_val(profile_name, 'CCV')
            }
        }

        # positing info to payment portal
        payment = 'https://elb.deposit.shopifycs.com/sessions'
        pay = requests.post(payment, json=payload, verify=False)

        if pay.status_code == requests.codes.ok:
            print('\nPayment authentication token - success.')

        else:
            print('\nPayment authentication token - failed.')
        
        # Payment token
        self.pay_token = json.loads(pay.text)['id']

    # Adds the specified products to cart
    def add_to_cart(self):

        self.session.get(self.cart_url)

        # Getting the cart and updating unique checkout link
        cart = self.session.get(self.checkout)
        self.checkout = cart.url

    # Enters personal information on checkout page
    def enter_personal(self):
        
        # Form Data
        payload = {
            '_method': 'patch',
            'authenticity_token': '', #auth_token,
            'previous_step': 'contact_information',
            'step': 'shipping_method',
            'checkout[email]': self.profile_dict.get_val(self.profile_name, 'Email'),
            'checkout[buyer_accepts_marketing]': '0',
            'checkout[buyer_accepts_marketing]': '1',
            'checkout[shipping_address][first_name]': self.profile_dict.get_val(self.profile_name, 'First Name'),
            'checkout[shipping_address][last_name]': self.profile_dict.get_val(self.profile_name, 'Last Name'),
            'checkout[shipping_address][address1]': self.profile_dict.get_val(self.profile_name, 'Address'),
            'checkout[shipping_address][address2]': self.profile_dict.get_val(self.profile_name, 'Address 2 (optional)'),
            'checkout[shipping_address][city]': self.profile_dict.get_val(self.profile_name, 'City'),
            'checkout[shipping_address][country]': self.profile_dict.get_val(self.profile_name, 'Country'),
            'checkout[shipping_address][province]': self.profile_dict.get_val(self.profile_name, 'Province'),
            'checkout[shipping_address][zip]': self.profile_dict.get_val(self.profile_name, 'Postal Code'),
            'checkout[shipping_address][phone]': self.profile_dict.get_val(self.profile_name, 'Phone'),
            'checkout[client_details][browser_width]': '1440',
            'checkout[client_details][browser_height]': '721',
            'checkout[client_details][javascript_enabled]': '1',
            'checkout[client_details][color_depth]': '30',
            'checkout[client_details][java_enabled]': 'true',
            'checkout[client_details][browser_tz]': '240',
            'checkout[remember_me]': '0',
            'button': ''
        }

        # Posting personal info to checkout page 
        r = self.session.post('{}'.format(self.checkout), data=payload) 

        print('\nPersonal info filled successfully.') if r.status_code == requests.codes.ok else print('\nPersonal info - failed.')

    # Gets and adds the cheapest shipping method
    def get_shipping(self):

        # Getting shipping
        shipping = 'https://{}/cart/shipping_rates.json?shipping_address[zip]={}&shipping_address[country]={}&shipping_address[province]={}'.format(self.domain, 'N5X0G6','Canada', 'ON')
        r = self.session.get(shipping, verify=False)

        if r.status_code == requests.codes.ok:
            # print('\nShipping page loaded - success.')

            try:
                # Shipping options
                shipping_options = json.loads(r.text)
                ship_opt = shipping_options['shipping_rates'][0]['name'].replace(' ', '%20')
                ship_rate = shipping_options['shipping_rates'][0]['price']
                option = 'shopify-{}-{}'.format(ship_opt,ship_rate)

                # Form Data
                ship = {
                    '_method':'patch',
                    'authenticity_token':'',
                    'previous_step':'shipping_method',
                    'step':'payment_method',
                    'checkout[shipping_rate][id]': option,
                    'button':'',
                    'checkout[client_details][browser_width]': '1440',
                    'checkout[client_details][browser_height]': '721',
                    'checkout[client_details][javascript_enabled]':'1'
                }

                # Posting info to the shipping page
                r = self.session.post(self.checkout, data=ship)

                print('\nShipping info filled successfully.') if r.status_code == requests.codes.ok else print('\nShipping info - failed.')

                # Retrieve payment gateway token
                try:
                    soup = bs(r.text, 'lxml')
                    self.pay_gate = soup.find('input', {'name':'checkout[payment_gateway]'})['value']
                    print('Payment Gate ID retreived')

                except Exception as e:
                    print('\nFailed to get the payment gateway token')
                    print(e)
            
            except IndexError:
                print('\nFailed to retrieve shipping info - Personal info not filled.')

        else:
            print('\nShipping page loaded - failed.')
                
    # Checkout the items in the cart
    def pay(self):

        # Credit card testing - Shopify
        # Declined message - 4000000000000002
        # Incorrect number - 4242424242424241
        # Disputed transaction - 4000000000000259
        # Invalid Expiry Month - 12 < 
        # Invalid Expiry Year - past year
        # Invalid CVV - any 2 digit

        # Form Data
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

        # Positing info to the payment page
        r = self.session.post(self.checkout + '?step=payment_method', data=payload)

        # Check for invalid cc info
        if b'Check your card' in r.content:
            print('\nCard information is invalid - Checkout failed')

        print('\nProcess complete.') if r.status_code == requests.codes.ok else print('\nProcess failed.')

        # Save page to html for confirmation
        with open('checkout.html', 'w') as file:
            file.write(r.text)

    # Runs entire checkout process
    def checkout_prod(self):
        print('Checkout initiated')
        start = time.time()
        self.load_payment()
        self.add_to_cart()
        self.enter_personal()
        self.get_shipping()
        self.pay()
        print('\nElapsed Time: %.2fs' % (time.time() - start))
