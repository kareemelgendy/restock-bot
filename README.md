# Restock Bot
A Python script that will scrape e-commerce websites powered by Shopify to periodically check for a product restock and update the user through SMS or automatically attempt to check out the item(s) being watched the moment they become available.

## Demo
For a more detailed demo <a href="https://www.dropbox.com/s/38xy47fs0lhklop/RestockBot%20Demo.mov?dl=0" target="_blank">click here</a>

<img src="./demo/demo.gif" height="500" style="height:auto; width:auto"/>

# TO DO
- [ ] Automate checkout
- [ ] Accept products with duplicate names
- [ ] Implement proxy support

# Important
- Make sure /products.json is accessible
- Enter Twilio API credentials to send SMS updates (notify.py)

### Required Modules
- beautifulsoup4
- webbrowser
- requests
- twilio
- time
- json
- lxml

# Getting Started

### Download The Repository
```sh
$ git clone https://github.com/kareemelgendy/RestockBot.git
$ cd RestockBot
```

### Install Required Modules
```sh
$ pip3 install -r txt/requirements.txt
```

### Remove Demo File (Optional)
```sh
$ rm -r demo
```

### Once all modules are installed and txt files are filled: 

In Terminal, change directory to the project folder and execute the following line to run the script:
```sh
$ python3 main.py
```

# Disclaimer
This program is a personal project and is not affiliated with Shopify in any way.
