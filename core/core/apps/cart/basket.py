

from decimal import Decimal
import math
from core.apps.products.models import Product


class Basket():
    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self, product, qty):
        
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {'product':product.title, 'price': str(product.price),'qty': int(qty)}

        self.session.modified = True
        
        
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['price'] = Decimal(item['item'])
            item['total_price'] = Decimal(item['price']) * Decimal(['qty'])
            yield item
        
    
    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())
        