from django.urls import path
from .views import (
    home, signup, travels, cart, reserved_travels, cancel_reservation,
    login_view, profile, reserve, success, updateprofil, Reservation,
    administrator_dashboard, client_list, delete_user, list_travels, delete_travel,
    add_promotion
)
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('updateprofil/', updateprofil, name='updateprofil'),
    path('', home, name='home'),
    path('home/', home, name='home_page'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('travels/', travels, name='travels'),
    path('search/', views.search_results, name='search_results'),
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('cart/', cart, name='cart'),
    path('travel_details/<int:travel_id>/', views.travel_details, name='travel_details'),
    path('reserve/<int:travel_id>/', reserve, name='reserve'),
    path('success/', success, name='success_page'),
    path('Reservation/', Reservation, name='Reservation'),
    path('reserved_travels/', reserved_travels, name='reserved_travels'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('administrator/', administrator_dashboard, name='administrator_dashboard'),
    path('clients/', client_list, name='client_list'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('list_travels/', list_travels, name='list_travels'),
    path('delete_travel/<int:travel_id>/', views.delete_travel, name='delete_travel'),
    path('clients/', client_list, name='client_list'),
    path('add_promotion/', add_promotion, name='add_promotion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
