from django.contrib import admin
from .models import Travel,Reservation
from django.contrib import admin
from .models import Promotion,CustomUser
admin.site.register(CustomUser)
admin.site.register(Promotion)

# Register your models here.
admin.site.register(Travel)
admin.site.register(Reservation)
