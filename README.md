# Restock Bot

A basic Python script that will scrape e-commerce websites powered by Shopify and periodically check for a product restock and update the user through SMS or automatically attempt to purchase the item(s) being watched the moment they become available.

## Important

- Make sure `/products.json` is accessible.
- Enter Twilio API credentials in an `.env` file for SMS notifications.

## Getting Started

1. Clone the repo or [click here](https://github.com/kareemelgendy/restock-bot/archive/refs/heads/main.zip)

```
$ git clone https://github.com/kareemelgendy/restock-bot.git
```

2. Install the required modules

```
$ cd restock-bot
$ pip3 install -r requirements.txt
```

3. Enter profiles (if any) in `data/profiles.json` and products in `data/products.json`.

   - Profiles are only used for product checkout if opted for.

**Example Profile:**

```
"John Doe": {
    "First Name": "John",
    "Last Name": "Doe",
    "Email": "johndoe@gmail.com",
    "Address": "23 Jump St.",
    "Address 2 (optional)": "",
    "City": "Toronto",
    "Province": "Ontario",
    "Country": "Canada",
    "Postal Code": "M5V 3L9",
    "Phone Number": "6471231234",
    "Payment": {
        "Card Number": "123456789012",
        "Name": "John Doe",
        "Expiry Date (MM/YY)": "12/34",
        "CVV": "123"
    }
}
```

**Example Product:**

- If an item has multiple sizes and/or colours fill accordingly, otherwise keep the fields blank.
  - Clothing: size (required), colour (optional)
  - Footwear: size (required), colour (optional)
  - Accessories: size (not applicable), colour (not applicable)
- If you wish to be notified by SMS, enter your phone number in the `Notification` field.
- If you would like to attempt to purchase the product automatically enter the profile name in the `Profile` field.
- `Product ID`, `Variant ID`, and `Cart URL` will all be filled automatically once you run main.py.
- In stock products will be moved to `data/in-stock.json`

```
"Black Bubble Owl Tee": {
    "Product URL": "https://ca.octobersveryown.com/collections/t-shirts/products/ss22-bubble-owl-t-shirt-black",
    "Size": "M",
    "Colour": "",
    "Product ID": "",
    "Variant ID": "",
    "Cart URL": "",
    "Profile": "John Doe",
    "Notification": ""
}
```

4. After entering profiles and products, run the following:

```
python3 main.py
```

## Disclaimer

The developer of this software should not be held liable for any lost opportunities resulting from its usage.
