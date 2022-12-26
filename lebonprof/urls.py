from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from core.views import acceuilpage
from core.views import apropos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('userprofile.urls')),
    path('',include('espaceannonce.urls')),
    path('', acceuilpage,name='acceuilpage'),
    path('apropos', apropos,name='apropos'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
