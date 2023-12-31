from django.urls import path
from .views import home, signup,travels,cart
from .views import login_view,profile,reserve,success
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    
    path('', home, name='home'),
    path('home/', home , name='home_page'),
    path('signup/', signup , name='signup'),
    path('profile/', profile , name='profile'),
    #path('login/', login , name='login'),
    path('travels/', travels, name='travels'),
    path('search/', views.search_results, name='search_results'),
    path('register/', views.signup, name='register'),
    path('login/',views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('cart/', cart, name='cart'),
    path('travel_details/<int:travel_id>/', views.travel_details, name='travel_details'),
    path('reserve/', reserve, name='reserve'), 
    path('success/', success, name='success_page')
 
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
