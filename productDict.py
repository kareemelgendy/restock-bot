
class Product:

    def __init__(self):
        self.products = dict()

    def newProduct(self, product_name, product_id, variant_id):
        self.product_name = product_name
        self.products[product_name] = {
            'Product ID': product_id,
            'Variant ID': variant_id
        }  

    def getProductName(self):
        return self.product_name

    def getProductID(self, product_name):
        return self.products[product_name]['Product ID']

    def getVariantID(self, product_name):
        return self.products[product_name]['Variant ID']

    def printProd(self, product_name):
        print('Product Name: ' + str(product_name))
        for keys in self.products[product_name]:
            print(str(keys) + ': ' + str(self.products[product_name][keys]))

    def printAll(self):
        for products in self.products:
            print(products)

    def size(self):
        return len(self.products)