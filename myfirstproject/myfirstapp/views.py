from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ReservationForm, SignUpForm, LoginForm, PromotionForm
from .models import Travel, CustomUser, Reservation, Promotion

def home(request):
    travels = Travel.objects.all()
    destinations = set([travel.destination for travel in travels])
    context = {
        'travels':travels,
        'destinations':destinations,
    }
    return render(request, 'myfirstapp/index.html',context)

def profile(request):
    my_reservations = Reservation.objects.filter(my_user=request.user)
    context = {
        'my_reservations': my_reservations,
    }

    return render(request, 'myfirstapp/profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home_page')
    else:
        form = SignUpForm()
    return render(request, 'myfirstapp/signup.html', {'form': form})

def cart(request):
    return render(request, 'myfirstapp/cart.html')

def success(request):
    return render(request, 'myfirstapp/success.html')

def travel_details(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    return render(request, 'myfirstapp/details.html', {'travel': travel})

def travels(request):
    travels = Travel.objects.all()
    travels = [apply_promotion(travel) for travel in travels]
    context = {
        'Travels': travels,
        'today': date.today()
        }

    return render(request, 'myfirstapp/travels.html', context)

def reservation_view(request):
    return render(request, 'myfirstapp/Reservation.html')

def search_results(request):
    if request.method == 'GET':
        max_price = request.GET.get('max_price')
        destination = request.GET.get('destination')
        duration = request.GET.get('duration')
        print(f"max_price: {max_price}, destination: {destination}, duration: {duration}")
        travels = Travel.objects.all()
        if max_price:
            travels = travels.filter(price__lte=max_price)
        if destination:
            travels = travels.filter(destination=destination)
        if duration:
            if duration == '1':
                travels = travels.filter(duration_days__lte=1)
            elif duration == '2':
                travels = travels.filter(duration_days__lte=4, duration_days__gte=2)
            elif duration == '3':
                travels = travels.filter(duration_days__gte=5, duration_days__lte=7)
            elif duration == '4':
                travels = travels.filter(duration_days__gte=8)
        travels = [apply_promotion(travel) for travel in travels]
        return render(request, 'myfirstapp/search_results.html', {'travels': travels})

def apply_promotion(travel):
    promotion = travel.promotion
    if promotion and (promotion.start_date <= date.today() <= promotion.end_date):
        travel.price -= travel.price * (promotion.discount_percentage / 100)
        travel.price  = round(travel.price, 2)
    return travel

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = LoginForm()
    return render(request, 'myfirstapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')

@login_required
def reserve(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.my_user = request.user
            reservation.travel = travel
            reservation.date = date.today()
            try:
                reservation.save()
                return redirect('success_page')
            except Exception as e:
                # Log the error here
                return render(request, 'error_template.html', {'message': 'Could not save reservation.'})
        else:
            # Form is not valid, render the form again with error messages
            return render(request, 'myfirstapp/profile.html', {'form': form, 'travel': travel})
    else:
        form = ReservationForm()
        return render(request, 'myfirstapp/profile.html', {'form': form, 'travel': travel})

@login_required(login_url="/login")
def updateprofil(request):
    if request.method == 'POST':
        user = request.user
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        username = request.POST.get('username')

        if firstname:
            user.first_name = firstname
        else:
            user.first_name = user.first_name

        if lastname:
            user.last_name = lastname
        else:
            user.last_name = user.last_name

        if birth_date:
            user.birth_date = birth_date
        else:
            user.birth_date = user.birth_date
        if email:
            user.email = email
        else:
            user.email = user.email
        if username:
            user.username = username
        else:
            user.username = user.username
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect("profile")
    return render(request, 'profile.html')

@login_required(login_url="/login")
def reserved_travels(request):
    reserved_travels = Travel.objects.filter(reservation__user=request.user)
    context = {
        'reserved_travels': reserved_travels,
    }
    return render(request, 'myfirstapp/Reservation.html', context)

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user == reservation.my_user:
        reservation.delete()
    # return to profile page
    return  redirect('profile')

@login_required
def administrator_dashboard(request):
    username = request.user.username
    last_five_users = get_user_model().objects.filter(is_superuser=False)[:5]
    all_admins = get_user_model().objects.filter(is_superuser=True)
    num_travels = Travel.objects.count()
    num_users = get_user_model().objects.filter(is_superuser=False).count()
    context = {
        'last_five_users': last_five_users,
        'all_admins': all_admins,
        'num_travels': num_travels,
        'num_users': num_users,
        'username': username,
    }
    return render(request, 'myfirstapp/administrateur.html', context)

def client_list(request):
    users = get_user_model().objects.filter(is_superuser=False)
    username = request.user.username
    context = {
        'username': username,
        'user_list': users,
    }
    return render(request, 'myfirstapp/Clients.html', context)

def delete_client(request, client_id):
    user = get_object_or_404(CustomUser, pk=client_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})

@login_required
def list_travels(request):
    travels = Travel.objects.all()
    travels = [apply_promotion(travel) for travel in travels]
    username = request.user.username
    context = {
        'username': username,
        'travel_list': travels
    }
    return render(request, 'myfirstapp/List_travels.html', context)

def delete_travel(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    travel.delete()
    return JsonResponse({'message': 'Travel deleted successfully'})

def add_promotion(request):
    promotions = Promotion.objects.all()
    context = {
        'promotions': promotions
    }
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save()
            selected_travel = form.cleaned_data['travel']
            selected_travel.promotion = promotion
            selected_travel.save()
            return render(request, 'myfirstapp/promotions.html',  {'form': form, **context})
    else:
        form = PromotionForm()
    context['username'] = request.user.username
    return render(request, 'myfirstapp/promotions.html',  {'form': form, **context})

def delete_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    promotion.delete()
    return JsonResponse({'message': 'Promotion deleted successfully'})

def add_travel(request):
    context = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        price = request.POST.get('price')
        destination = request.POST.get('destination')
        duration_days = request.POST.get('duration_days')
        image = request.FILES.get('image')
        travel = Travel(city=city, price=price, destination=destination, duration_days=duration_days, image=image)
        travel.save()
        return redirect('list_travels')
    else:
        return render(request, 'myfirstapp/List_travels.html', context)
    
def edit_travel(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    if request.method == 'POST':
        city = request.POST.get('edit_city')
        price = request.POST.get('edit_price')
        destination = request.POST.get('edit_destination')
        duration_days = request.POST.get('edit_duration_days')
        image = request.FILES.get('edit_image')
        travel.city = city
        travel.price = price
        travel.destination = destination
        travel.duration_days = duration_days
        travel.image = image
        travel.save()
        return render(request, 'myfirstapp/List_travels.html', {'travel': travel})
    else:
        return render(request, 'myfirstapp/List_travels.html', {'travel': travel})
    