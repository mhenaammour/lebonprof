from django.db.models import Q
from django.shortcuts import render,get_object_or_404, redirect
from .cart import Cart
from .models import Annonce
import requests
import json
from django.contrib.gis.geos import Point
import geocoder
from .forms import OfferForm
from django.contrib.auth.decorators import login_required











def add_to_fav(request, annonce_id):
    cart=Cart(request)
    cart.add(annonce_id)

    return redirect('/')


def remove_from_fav(request, annonce_id):
    cart=Cart(request)
    cart.remove(str(annonce_id))

    return redirect('/')
    
def fav_view(request):
    cart=Cart(request)

    return render(request , 'espaceannonce/fav_view.html', {'cart':cart})



def search(request):
    query=request.GET.get('q')
    if query:
        annonces=Annonce.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    else :
        annonces=Annonce.objects.all()

    return render(request,'espaceannonce/search.html',{'annonces':annonces})
    



def annonce_detail(request,slug):
    annonce=get_object_or_404(Annonce , slug=slug)
    point = geocoder.google(annonce.addresse).point  


    return render(request,"espaceannonce/annonce_detail.html",{'annonce':annonce,'static': 'static'})





def fav_detail(request,slug):
    annonce=get_object_or_404(Annonce , slug=slug)
    return render(request,"espaceannonce/fav_detail.html",{'annonce':annonce})




@login_required
def submit_offer(request, annonc_id):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.vendor = request.user
            offer.annonc_id = annonc_id
            offer.save()
            return redirect('/confirmation/')
    else:
        form = OfferForm()
    return render(request, 'espaceannonce/submit_offer.html', {'form': form})

def offer_confirmation(request):
    return render(request, 'espaceannonce/offer_confirmation.html')
