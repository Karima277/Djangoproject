from django.urls import path
from .views import home, signup, login,travels

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('home/', home , name='home_page'),
    path('signup/', signup , name='signup'),
    path('login/', login , name='login'),
    path('travels/', travels, name='travels'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
