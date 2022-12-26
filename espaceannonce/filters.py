import django_filters
from .models import Annonce

class AnnonceFilter(django_filters.FilterSet):

    class meta:
        model=Annonce
        fields={'category':['exact']}

