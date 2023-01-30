from django.urls import path
from . import views

urlpatterns = [

    path('search/' ,views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('get_communes/', views.get_communes, name='get_communes'),

    path('add_to_fav/<int:annonce_id>/',views.add_to_fav,name='add_to_fav'),
    path('remove_from_fav/<str:annonce_id>/',views.remove_from_fav,name='remove_from_fav'),
    path('fav/', views.fav_view, name='fav_view'),
    path('confirmation/', views.offer_confirmation, name='offer_confirmation'),
    path('Message_confirmation/', views.message_confirmation, name='message_confirmation'),

    path('<slug:slug>/',views.annonce_detail,name='annonce_detail'),

    path('fav_detail/<slug:slug>/',views.fav_detail,name='fav_detail'),

    path('submit/<int:annonc_id>/', views.submit_offer, name='submit_offer'),
    path('submitmessage/<int:annonce_id>/<int:seller_id>/', views.submit_message, name='submit_message'),



    

]
