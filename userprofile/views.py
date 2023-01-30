from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import Userprofile
from espaceannonce.forms import AnnonceForm
from espaceannonce.models import Annonce,MessageAnn
from django.utils.text import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.http import HttpResponse , Http404 , HttpResponseNotFound
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from .forms import CustomUserCreationForm



@login_required
def scrape_view(request):
    #Send an HTTP request to the website and retrieve the HTML content#
    URL = 'https://www.superprof.ch/s/toute-matiere,Suisse,,.html'

    response = requests.get( URL)
    html_content = response.content

    #Parse the HTML content using Beautiful Soup#
    soup = BeautifulSoup(html_content, 'html.parser')

    #Extract the data from the HTML using Beautiful Soup#
    titles = soup.find_all('h2', class_='titre')
    prices = soup.find_all('span', class_='label')
    adresses = soup.find_all('p', class_='adresse')

    #Store the data in a list of dictionaries#
    data = []
    for i in range(len(titles)):
        data.append({
            'title': titles[i].text,
            'price': prices[i].text,
            'adresse': adresses[i].text,
        })

    #Render the data in a template#
    return render(request, 'userprofile/scrape.html', {'data': data})




@login_required
def mesannonces(request):
#cette fonction sert a afficher les annonces publié par un certain utilisateur il devra etre authentifié 
#
    return render(request,'userprofile/mesannonces.html')

@login_required
def mesmessages(request):
	#cette fonction affiche les messages d'un utilisateur donné il devra etre authentifié
	#
    logged=request.user
    messages=MessageAnn.objects.filter(seller=request.user).order_by('created_at')
    return render(request,'userprofile/messages.html',{'messages':messages})

@login_required
def add_annonce(request):
#cette fonction permet a un utilisateur de publier une annonce sur le site il devra etre authentifié#
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
#cette fonction permet de modifier une annonce donnée , l'utilisateur  doit etre authentifié#
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
#cette fonction permet de supprimer une annonce, 'utilisateur  doit etre authentifié#
    annonce=Annonce.objects.filter(user=request.user).get(slug=slug)
    annonce.delete()
    messages.success(request , 'Votre annonce a bien été supprimer')
    return HttpResponseRedirect(reverse('/'))








def annonceur_detail(request,pk):
#cette fonction affiche les details sur un annonceur , son nom , prenom , adresse...#
    user=User.objects.get(pk=pk)
    return render(request,"userprofile/annonceur_detail.html",{'user':user})

def buyer_detail(request,pk):
#cette fonction permet d'afficher les infos d'une personne qui est interesser par l'annonce#
    user=Userprofile.objects.get(user=request.user)
    return render(request, 'userprofile/buyer_detail.html',{'user':user})

#cette fonction affiche les informations de l utilisateur connecter dans la section moncompt#
@login_required
def moncompte(request):
    profile=Userprofile.objects.get(user=request.user)
    return render(request,'userprofile/moncompte.html',{'profile':profile})
#cette fonction permet a un utilisateur de s'inscrire a notre site en remplissant tous les champs #
def signup(request):
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST,request.FILES)

        if form.is_valid():
            user=form.save()
            login(request ,user,backend='django.contrib.auth.backends.ModelBackend')
            userprofile=Userprofile.objects.create(user=user, first_name = form.cleaned_data.get('first_name'), last_name = form.cleaned_data.get('last_name'), phone_number = form.cleaned_data.get('phone_number'), profile_picture = form.cleaned_data.get('profile_picture'))
            return redirect('/')

    else:
        form=CustomUserCreationForm()
    
        
    return render(request, "userprofile/signup.html",{'form':form})

import asyncio

def scrape_data(request):
#cette fonction permet a l'admin du site de lancer une operation de web scrapping du site 'www.apprentus.com' elle scrappe 100 page et elle envoie les données qui sont des données scolaires dans un fichier excel#
    async def get_page(s, url):
        async with s.get(url) as response:
            return await response.text()

    async def get_all_pages(s, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_page(s, url))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
        return res

    def get_cours_infos(soup):
        result = []

        cours = soup.select('div > div.text')
        print(len(cours))
        for cour in cours:
            try:
                name = extract_info(
                    cour, 'div.name-rating-row > a')
                status = extract_info(
                    cour, 'div.result-content > a > span.premium-teacher')
                location = extract_info(
                    cour, 'div.name-rating-row > a > span')
                modulesContainer = cour.select('div.result-tags')
                modules = []
                try:
                    for module in modulesContainer:
                        moduleTeached = extract_info(
                            module, f'div.result-tags > span:nth-child({modulesContainer.index(module) + 1})')
                        modules.append(moduleTeached)
                except:
                    print('cant get modules')

                title = extract_info(
                    cour, 'div.title-price-row > div > a > span')

                description = extract_info(
                    cour, 'div.result-content > a > span:nth-child(2)')

                price = extract_info(
                    cour, 'div.title-price-row > div > span > span')
                modules = str(modules).replace('[', '').replace(']', '')
                name = eliminate_special_characters(name)
                name = extract_name_from_text(name)
                modules = eliminate_special_characters(modules)
                result.append({
                    'name': name,
                    'status': status,
                    'modules': modules,
                    'location': location,
                    'title': title,
                    'description': description,
                    'price': price,
                })

            except:
                print('cant get info')
        if (os.path.exists('cours.xlsx')):
            df = pd.read_excel('cours.xlsx')
            df = pd.concat([df, pd.DataFrame(result).drop_duplicates()])
            df.to_excel('cours.xlsx', index=False)
        else:
            df = pd.DataFrame(result).drop_duplicates()
            df.to_excel('cours.xlsx', index=False)

    def eliminate_special_characters(text):
        return re.sub('[^A-Za-z0-9]+', ' ', text)

    def extract_name_from_text(text):
        return text.split(' ')[0]

    def extract_info(soup, element):
        info = soup.select(element)
        if info:
            return info[0].text.strip()
        else:
            return ''

    async def data_scraper():
        urls = range(1, 100)
        urls = [
            f'https://www.apprentus.com/fr/s/Bejaia-Algerie/Soutien-scolaire/36.5574,4.7692/13/25/{url}/' for url in urls]
        async with aiohttp.ClientSession() as s:
            htmls = await get_all_pages(s, urls)
            for html in htmls:
                print(f'scrapping page {htmls.index(html) + 1}')
                soup = BeautifulSoup(html, 'html5lib')
                get_cours_infos(soup)

    asyncio.run(data_scraper())
    return response("Scraping done", status=status.HTTP_200_OK)


def download_scraped_data(request):
#cette fonction permet de telecharger le fichier excel generer par la fonction de web scrapping#
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    path = 'cours.xlsx'
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(path)
            return response
    raise Http404



   
