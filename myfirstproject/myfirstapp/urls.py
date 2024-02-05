from django.urls import path
from .views import (
    home, signup, travels, cart, reserved_travels, cancel_reservation,
    login_view, profile, reserve, success, updateprofil, reservation_view,
    administrator_dashboard, client_list, list_travels, delete_travel,
    delete_client,add_promotion,logout_view
)
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # general paths
    path('updateprofil/', updateprofil, name='updateprofil'),
    path('', home, name='home'),
    path('home/', home, name='home_page'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('search/', views.search_results, name='search_results'),
    path('register/', views.signup, name='register'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('cart/', cart, name='cart'),
    path('success/', success, name='success_page'),
    path('administrator/', administrator_dashboard, name='administrator_dashboard'),
    



    # travels
    path('travels/', travels, name='travels'),
    path('list_travels/', list_travels, name='list_travels'),
    path('add_travel/', views.add_travel, name='add_travel'),
    path('edit_travel/<int:travel_id>/', views.edit_travel, name='edit_travel'),
    path('delete_travel/<int:travel_id>/', views.delete_travel, name='delete_travel'),
    path('travel_details/<int:travel_id>/', views.travel_details, name='travel_details'),

    # clients
    path('clients/', client_list, name='client_list'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),

    # promotions
    path('add_promotion/', add_promotion, name='add_promotion'),
    path('delete_promotion/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    
    # reservations
    path('Reservation/', reservation_view, name='Reservation'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('reserved_travels/', reserved_travels, name='reserved_travels'),
    path('reserve/<int:travel_id>/', reserve, name='reserve'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
