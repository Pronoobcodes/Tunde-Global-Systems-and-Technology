from store.models import Product
from custom_auth.models import Customer

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')  

        
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Customer.objects.filter(user__id=self.request.user.id)
            cartt = str(self.cart).replace("\'", "\"")
            user.update(user_cart=str(cartt))

    def db_add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=[int(i) for i in product_ids])
        return products

    def get_qyt(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        cart = self.cart
        cart[product_id] = product_qty
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Customer.objects.filter(user__id=self.request.user.id)
            cartt = str(self.cart).replace("\'", "\"")
            user.update(user_cart=str(cartt))

        ret = self.cart
        return ret
    
    def delete(self, product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Customer.objects.filter(user__id=self.request.user.id)
            cartt = str(self.cart).replace("\'", "\"")
            user.update(user_cart=str(cartt))

        ret = self.cart
        return ret

    def cart_total(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(id__in=product_id)
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
    
    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
        self.session.modified = True
        self.cart = {}

        if self.request.user.is_authenticated:
            user = Customer.objects.filter(user__id=self.request.user.id)
            user.update(user_cart="")
            
        return self.cart