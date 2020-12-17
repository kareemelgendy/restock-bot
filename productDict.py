
class Product:

    # Constructor
    def __init__(self):
        self.products = dict()

    # Initializing a new product 
    def newProduct(self, product_name):
        self.product_name = product_name
        self.products[product_name] = {
            'Product ID': None,
            'Variant ID': None, 
            'Cart URL': None,
            'Profile': None
        }  
    
    # Sets the value of a key
    def setVal(self, product_name, target_key, newValue):
        product = self.products[product_name]
        for value in product:
            if value == target_key:
                product[target_key] = newValue
                break
    
    # Prints the products keys and value
    def printProd(self, product_name):
        print('Product Name: ' + str(product_name))
        for keys in self.products[product_name]:
            print(str(keys) + ': ' + str(self.products[product_name][keys]))

    # Prints all products
    def printAll(self):
        for products in self.products:
            print(products)

    # Returns the size of the dictionary
    def size(self):
        return len(self.products)