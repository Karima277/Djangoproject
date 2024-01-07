"""
URL configuration for myfirstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static  import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myfirstapp.urls')),
    path('home/', include('myfirstapp.urls')),
    path('travels/', include('myfirstapp.urls')),
    path('signup/', include('myfirstapp.urls')),
    path('login/', include('myfirstapp.urls')),
    path('profile/', include('myfirstapp.urls')),
    path('logout/', include('myfirstapp.urls')),
    path('clients//', include('myfirstapp.urls')),
    path('list_travels/', include('myfirstapp.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
