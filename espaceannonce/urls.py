from django.urls import path
from . import views

urlpatterns = [
    path('search/' ,views.search, name='search'),
    path('add_to_fav/<int:annonce_id>/',views.add_to_fav,name='add_to_fav'),
    path('remove_from_fav/<str:annonce_id>/',views.remove_from_fav,name='remove_from_fav'),
    path('fav/', views.fav_view, name='fav_view'),
    path('<slug:slug>/',views.annonce_detail,name='annonce_detail'),
    path('fav_detail/<slug:slug>/',views.fav_detail,name='fav_detail'),


    

]