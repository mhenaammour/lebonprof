from django.shortcuts import render
from espaceannonce.models import Annonce
from espaceannonce.models import Wilaya
from django.utils.text import slugify
#ceci est la fonction qui retourne toutes les annonces ordonner selon la date de publication
def acceuilpage(request):
    annonces=Annonce.objects.all().order_by("-date_pub")

    return render(request,'core/acceuilpage.html',{'annonces':annonces})
    
#cette page affiche des infos suplementaire sur le site#
def apropos(request):
    print("succefuliy created wilaays")       
    return render(request,'core/apropos.html')
