
class Product:

    # Constructor
    def __init__(self):
        self.products = dict()

    # Initializing a new product 
    def newProduct(self, product_name):
        self.product_name = product_name
        self.products[product_name] = {
            'Product URL': None,
            'Product ID': None,
            'Variant ID': None, 
            'Cart URL': None,
            'Profile': None
        } 

    def getDict(self):
        return self.products

    def removeProduct(self, product_name):
        del self.products[product_name]

    # Sets the value of a key
    def setVal(self, product_name, target_key, newValue):
        product = self.products[product_name]
        for value in product:
            if value == target_key:
                product[target_key] = newValue
                break

    # Returns value of a key in given product
    def getVal(self, product_name, key):
        return self.products[product_name][key]

    # Prints the products keys and value
    def printProdInfo(self, product_name):
        print('Product Name: ' + str(product_name))
        for keys in self.products[product_name]:
            print(str(keys) + ': ' + str(self.products[product_name][keys]))

    # Prints all products
    def printProducts(self):
        for products in self.products:
            print(products)

    def printAll(self):
        for products in self.products:
            print('Product Name: ' + str(products))
            for keys in self.products[products]:
                print('\t' + str(keys) + ': ' + str(self.products[products][keys]))

    # Returns the size of the dictionary
    def size(self):
        return len(self.products)


# p = Product()
# name1 = 'CLASSIC OWL HOODIE - BLACK'
# pid = '4621388677185'
# vid = '29539163013185'
# cart = 'https://ca.octobersveryown.com/cart/update?updates[' + str(vid) + ']=1'

# p.newProduct(name1)
# p.setVal(name1, 'Product URL', 'https://ca.octobersveryown.com/products/classic-owl-hoodie-black')
# p.setVal(name1, 'Product ID', pid)
# p.setVal(name1, 'Variant ID', vid)
# p.setVal(name1, 'Cart URL', cart)

# print(p.getAvailability(name1))

# name2 = 'CLASSIC OWL HOODIE - WHITE'

# p.newProduct(name2)
# p.setVal(name2, 'Product URL', 'https://ca.octobersveryown.com/products/classic-owl-hoodie-black')
# p.setVal(name2, 'Product ID', pid)
# p.setVal(name2, 'Variant ID', '29543280934977')
# p.setVal(name2, 'Cart URL', 'https://ca.octobersveryown.com/cart/update?updates[32299384045633]=1')

# print(p.getAvailability(name2))