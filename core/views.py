from django.shortcuts import render
from espaceannonce.models import Annonce

def acceuilpage(request):
    annonces=Annonce.objects.all().order_by("-date_pub")

    return render(request,'core/acceuilpage.html',{'annonces':annonces})

def apropos(request):
    return render(request,'core/apropos.html')