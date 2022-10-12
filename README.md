# Restock Bot

A basic Python script that will scrape e-commerce websites powered by Shopify and periodically check for a product restock and update the user through SMS using the Twilio API or automatically attempt to purchase the item(s) being watched the moment they become available.

## Important

- Make sure `/products.json` is accessible
- Enter Twilio API credentials in an `.env` file for SMS notifications

## Checkout Testing

**Shopify checkout test cases:**

- Declined message - 4000000000000002
- Incorrect number - 4242424242424241
- Disputed transaction - 4000000000000259
- Invalid Expiry Month - 12 < XX
- Invalid Expiry Year - past year
- Invalid CVV - any 2 digits

## Getting Started

1. Clone the repo

```
$ git clone https://github.com/kareemelgendy/restock-bot.git
```

2. Create and activate virtual environment
   
   Install virtualenv: `sudo pip install virtualenv` if needed

```
$ cd restock-bot
$ virtualenv env
$ source env/bin/activate
```

3. Create an `.env` file for the Twilio SMS API keys (if using SMS)

```
$ touch .env
$ source .env
```

4. Install the required modules

```
$ pip install -r requirements.txt
```

5. Enter profiles (if any) in `data/profiles.json` and products in `data/products.json`
   - Profiles are only used for product checkout if opted for

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

- If an item has multiple sizes and/or colours fill accordingly, otherwise keep the fields blank
  - **Clothing**: size (required), colour (optional)
  - **Footwear**: size (required), colour (optional)
  - **Accessories**: size (not applicable), colour (not applicable)
- Fill `Phone` field if you wish to be notified by SMS
- Fill `Profile` field with a valid profile if you want to attempt to checkout

**If both `Profile` and `Phone` fields are filled, `Profile` will take precendence

```
{
	"Product URL": "https://ca.octobersveryown.com/collections/t-shirts/products/ss22-bubble-owl-t-shirt-black",
	"Size": "M",
	"Colour": "",
	"Profile": "John Doe",
	"Phone": ""
}
```

4. After entering profiles and products, run the following:

```
python main.py
```

## Disclaimer

The developer of this software should not be held liable for any lost opportunities resulting from its usage.
