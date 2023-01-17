from django.contrib import admin

from .models import Category
from .models import Theme
from .models import Modalité
from .models import Commune
from .models import Wilaya
from .models import Annonce
from .models import Offer
admin.site.register(Wilaya)
admin.site.register(Category)
admin.site.register(Theme)
admin.site.register(Commune)
admin.site.register(Modalité)
admin.site.register(Annonce)
admin.site.register(Offer)