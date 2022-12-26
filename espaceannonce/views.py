from django.db.models import Q
from django.shortcuts import render,get_object_or_404, redirect
from .cart import Cart
from .models import Annonce









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
    return render(request,"espaceannonce/annonce_detail.html",{'annonce':annonce})

def fav_detail(request,slug):
    annonce=get_object_or_404(Annonce , slug=slug)
    return render(request,"espaceannonce/fav_detail.html",{'annonce':annonce})