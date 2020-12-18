
class Product:

    # Constructor
    def __init__(self):
        self.products = dict()

    # Initializing a new product 
    def new_product(self, product_name):
        self.product_name = product_name
        self.products[product_name] = {
            'Product URL': None,
            'Product ID': None,
            'Variant ID': None, 
            'Cart URL': None,
            'Profile': None
        } 

    # Returns the dictionary
    def get_dict(self):
        return self.products

    # Removes a product 
    def remove_product(self, product_name):
        del self.products[product_name]

    # Sets the value of a key
    def set_val(self, product_name, target_key, newValue):
        product = self.products[product_name]
        for value in product:
            if value == target_key:
                product[target_key] = newValue
                break

    # Returns value of a key in given product
    def get_val(self, product_name, key):
        return self.products[product_name][key]

    # Prints the products keys and value
    def print_prod_info(self, product_name):
        print('Product Name: ' + str(product_name))
        for keys in self.products[product_name]:
            print(str(keys) + ': ' + str(self.products[product_name][keys]))

    # Prints all products
    def print_products(self):
        for products in self.products:
            print(products)

    # Prints all products and their information
    def print_all(self):
        for products in self.products:
            print('Product Name: ' + str(products))
            for keys in self.products[products]:
                print('\t' + str(keys) + ': ' + str(self.products[products][keys]))

    # Returns the size of the dictionary
    def size(self):
        return len(self.products)

    # Returns if the dictionary is empty
    def is_empty(self):
        if len(self.products) == 0:
            return True
        else:
            return False
