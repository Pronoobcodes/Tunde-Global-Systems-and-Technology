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
        
        try:
            product_id = str(product.id)
            product_qty = int(quantity)

            # Validate quantity
            if product_qty <= 0 or product_qty > 5:
                return None

            if product_id in self.cart:
                new_qty = self.cart[product_id] + product_qty
                if new_qty > 5:
                    new_qty = 5
                self.cart[product_id] = new_qty
            else:
                self.cart[product_id] = product_qty

            self.session.modified = True

            if self.request.user.is_authenticated:
                user = Customer.objects.filter(id=self.request.user.id)
                cart_str = str(self.cart).replace("\'", "\"")
                user.update(user_cart=cart_str)

            return self.cart
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return None

    def db_add(self, product, quantity):
        
        try:
            product_id = str(product.id)
            product_qty = int(quantity)

            if product_qty <= 0 or product_qty > 5:
                return None

            if product_id not in self.cart:
                self.cart[product_id] = product_qty

            self.session.modified = True
            return self.cart
        except Exception as e:
            print(f"Error adding to cart from DB: {e}")
            return None

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
        """Update quantity of a product in cart"""
        try:
            product_qty = int(quantity)
            if product_qty <= 0 or product_qty > 5:
                return None

            product_id = str(product.id)
            
            self.cart[product_id] = product_qty
            self.session.modified = True

           
            if self.request.user.is_authenticated:
                user = Customer.objects.filter(id=self.request.user.id)
                cart_str = str(self.cart).replace("\'", "\"")
                user.update(user_cart=cart_str)

            return self.cart
        except Exception as e:
            print(f"Error updating cart: {e}")
            return None
    
    def delete(self, product):
        """Delete an item from the cart"""
        try:
            product_id = str(product)  
            
            if product_id in self.cart:
                del self.cart[product_id]

            self.session.modified = True

            if self.request.user.is_authenticated:
                user = Customer.objects.filter(id=self.request.user.id)
                cart_str = str(self.cart).replace("\'", "\"")
                user.update(user_cart=cart_str)

            return self.cart
        except Exception as e:
            print(f"Error deleting from cart: {e}")
            return self.cart

    def cart_total(self):
        try:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=[int(i) for i in product_ids])
            total = 0
            for product in products:
                qty = int(self.cart[str(product.id)])
                price = float(product.sale_price if product.is_sale else product.price)
                total += price * qty
            return round(total, 2)
        except Exception as e:
            print(f"Error calculating cart total: {e}")
            return 0.0
    
    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
        self.session.modified = True
        self.cart = {}

        if self.request.user.is_authenticated:
            user = Customer.objects.filter(id=self.request.user.id)
            user.update(user_cart="")
            
        return self.cart