from django.db.models import Q
from django.shortcuts import render,get_object_or_404, redirect
from .cart import Cart
from .models import Annonce,Commune
import requests
import json
from django.contrib.gis.geos import Point
import geocoder
from .forms import OfferForm,MessageForm,SearchFilterForm
from django.contrib.auth.decorators import login_required
import difflib



def search_results(request):
# The view for displaying search results
    form = SearchFilterForm(request.GET)

    if form.is_valid():
        wilaya = form.cleaned_data['wilaya']
        commune = form.cleaned_data['commune']
        theme = form.cleaned_data['module']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        annonces = Annonce.objects.all()

        if wilaya:
            annonces = annonces.filter(wilaya=wilaya)

        if commune:
            annonces = annonces.filter(commune=commune)

        if start_date:
            annonces = annonces.filter(date_pub__gte=start_date)
        if end_date:
            annonces = annonces.filter(date_pub__lte=end_date)
        if theme:
            annonces = annonces.filter(theme__title__icontains=theme)

        return render(request, 'espaceannonce/search_results.html', {'form': form, 'annonces': annonces})

    return render(request, 'espaceannonce/search_form.html', {'form': form})



from django.http import JsonResponse

def get_communes(request):
# cette fonctions a pour but d afficher pour chaque wilaya ses communes associées#
    wilaya_id = request.GET.get('wilaya_id')
    communes = Commune.objects.filter(wilaya_id=wilaya_id).values('id', 'title')
    return JsonResponse({'communes': list(communes)})








def add_to_fav(request, annonce_id):
#cette fonction permet a l utilisateur d ajouter une annonce a sa liste de favories#
    cart=Cart(request)
    cart.add(annonce_id)

    return redirect('/')


def remove_from_fav(request, annonce_id):
#permet de retirer une annonce de sa liste de favories#
    cart=Cart(request)
    cart.remove(str(annonce_id))

    return redirect('/')

def fav_view(request):
#elle permet d afficher la liste des annonces favories d un utilisateur#
    cart=Cart(request)

    return render(request , 'espaceannonce/fav_view.html', {'cart':cart})



def search(request):
#elle nous permet de rechercher une annonce selon son titre et sa description#
    query=request.GET.get('q')
    if query:
        annonces=Annonce.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    else :
        annonces=Annonce.objects.all()

    return render(request,'espaceannonce/search.html',{'annonces':annonces})
    



def annonce_detail(request,slug):
#elle sert a afficher les details d une annonce#
    annonce=get_object_or_404(Annonce , slug=slug)
    point = geocoder.google(annonce.addresse).point  


    return render(request,"espaceannonce/annonce_detail.html",{'annonce':annonce,'static': 'static'})





def fav_detail(request,slug):
#elle permet de retourner les details de mes annonces  favorites#
    annonce=get_object_or_404(Annonce , slug=slug)
    return render(request,"espaceannonce/fav_detail.html",{'annonce':annonce})



@login_required
def submit_offer(request, annonc_id):
#elle permet a un utilisateur de laisser un commentaire sur une annonce donnée#
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

@login_required
def submit_message(request, annonce_id, seller_id):
#elle permet a l utilisateur de laisser un messsage au detenteur de l annonce#
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.buyer = request.user
            msg.seller_id=seller_id
            msg.annonce_id = annonce_id
            msg.save()
            return redirect('/Message_confirmation/')
    else:
        form = MessageForm()
    return render(request, 'espaceannonce/submit_message.html', {'form': form})

def offer_confirmation(request):
#elle permet d afficher un messsage de confirmation une foie qu'un utilisateur laisse un commentaire#
    return render(request, 'espaceannonce/offer_confirmation.html')

def message_confirmation(request):
#elle permet d afficher un messsage de confirmation une foie qu'un utilisateur laisse un message#
    return render(request , 'espaceannonce/message_confirmation.html')
