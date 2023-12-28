from django.urls import path
from .views import home  # Assurez-vous d'importer vos vues correctement

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
