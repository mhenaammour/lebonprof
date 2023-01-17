from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import Userprofile
from espaceannonce.forms import AnnonceForm
from espaceannonce.models import Annonce
from django.utils.text import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from bs4 import BeautifulSoup


@login_required
def scrape_view(request):
    # Send an HTTP request to the website and retrieve the HTML content
    URL = 'https://www.superprof.ch/s/toute-matiere,Suisse,,.html'

    response = requests.get( URL)
    html_content = response.content

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the data from the HTML using Beautiful Soup
    titles = soup.find_all('h2', class_='titre')
    prices = soup.find_all('span', class_='label')
    adresses = soup.find_all('p', class_='adresse')

    # Store the data in a list of dictionaries
    data = []
    for i in range(len(titles)):
        data.append({
            'title': titles[i].text,
            'price': prices[i].text,
            'adresse': adresses[i].text,
        })

    # Render the data in a template
    return render(request, 'userprofile/scrape.html', {'data': data})

@login_required
def mesannonces(request):
    return render(request,'userprofile/mesannonces.html')

@login_required
def add_annonce(request):
    if request.method == 'POST':
        form=AnnonceForm(request.POST, request.FILES)

        if form.is_valid():
            title=request.POST.get('title')
            annonce=form.save(commit=False)
            annonce.user = request.user
            annonce.slug = slugify(title)

            annonce.save()
            messages.success(request , 'Votre annonce est postée avec succes !')
            return redirect('/')
    else:
        form=AnnonceForm()
        titre='Ajouter'

    return render(request,'userprofile/add_annonce.html',{'form':form,'titre':titre})

@login_required
def edit_annonce(request, pk):
    annonce=Annonce.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form=AnnonceForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            messages.success(request , 'Votre annonce a été modifié avec succes !')

            return redirect('/')

    else:
        form=AnnonceForm(instance=annonce)
    titre='Modifier'
    return render(request,'userprofile/add_annonce.html',{'form':form,'titre':titre})

@login_required
def delete_annonce(request,slug):
    annonce=Annonce.objects.filter(user=request.user).get(slug=slug)
    annonce.delete()
    messages.success(request , 'Votre annonce a bien été supprimer')
    return HttpResponseRedirect(reverse('/'))








def annonceur_detail(request,pk):
    user=User.objects.get(pk=pk)
    return render(request,"userprofile/annonceur_detail.html",{'user':user})


@login_required
def moncompte(request):
    return render(request,'userprofile/moncompte.html')

def signup(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request ,user,backend='django.contrib.auth.backends.ModelBackend')
            userprofile=Userprofile.objects.create(user=user)
            return redirect('/')

    else:
        form=UserCreationForm()
    
        
    return render(request, "userprofile/signup.html",{'form':form})

