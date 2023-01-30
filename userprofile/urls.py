from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),

    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    path('moncompte/',views.moncompte,name='moncompte'),
    path('mesannonces/',views.mesannonces,name='mesannonces'),
    path('mesannonces/add_annonce/',views.add_annonce,name='add_annonce'),
    path('mesannonces/edit_annonce/<int:pk>/',views.edit_annonce,name='edit_annonce'),
    path('mesannonces/delete_annonce/<slug:slug>/',views.delete_annonce,name='delete_annonce'),

    path('annonceur/<int:pk>/', views.annonceur_detail,name='annonceur_detail'),
    path('scrappedannonces/',views.scrape_view, name='scrapper'),
    path('scraper/', views.scrape_data, name='scrappe'),
    path('download/', views.download_scraped_data, name='download'),
    path('Mesmessages/',views.mesmessages , name='mesmessages'),
    path('buyer/<int:pk>/', views.buyer_detail,name='buyer_detail'),



]
