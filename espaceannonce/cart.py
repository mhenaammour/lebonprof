from django.conf import settings
from .models import Annonce 

class Cart(object):
    def __init__(self, request):
        self.session= request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}

        self.cart=cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['annonce']= Annonce.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price']= 100/100
            yield item

     
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified= True

    def add(self , annonce_id, quantity=1 ,update_quantity=False):
        annonce_id=str(annonce_id)

        if annonce_id not in self.cart:
            self.cart[annonce_id]={'quanity': int(quantity), 'id':annonce_id}

        if update_quantity:
            self.cart[annonce_id]['quantity']+= int(quantity)

        self.save()

    def remove(self, annonce_id):
        if str(annonce_id) in self.cart:
            del self.cart[str(annonce_id)]

            self.save()

