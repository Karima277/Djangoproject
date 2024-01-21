from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm, PromotionForm
from .models import Travel, CustomUser, Reservation

def home(request):
    return render(request, 'myfirstapp/index.html')

def profile(request):
    return render(request, 'myfirstapp/profile.html')

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
    context = {'Travels': Travel.objects.all()}
    return render(request, 'myfirstapp/travels.html', context)

def Reservation(request):
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
            try:
                if '-' in duration:
                    start, end = map(int, duration.split('-'))
                    travels = travels.filter(duration_days__gte=start, duration_days__lte=end)
                else:
                    duration_int = int(duration)
                    travels = travels.filter(duration_days=duration_int)
            except ValueError:
                pass
        print(f"Number of travels after filtering: {travels.count()}")
        return render(request, 'myfirstapp/search_results.html', {'travels': travels})

def apply_promotion(travel):
    promotion = travel.promotion
    if promotion and promotion.start_date <= date.today() <= promotion.end_date:
        travel.price -= travel.price * (promotion.discount_percentage / 100)
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
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        card_number = request.POST.get('cardnumber')
        expiration_date = request.POST.get('expiration')
        cvv = request.POST.get('cvv')
        reservation = Reservation(
            my_user=request.user,
            travel=travel,
            date=date.today()
            )
        reservation.save()
        return redirect('success_page')
    return render(request, 'your_template.html', {'travel': travel})

@login_required(login_url="/login")
def updateprofil(request):
    if request.method == 'POST':
        user = request.user
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        user.first_name = firstname
        user.last_name = lastname
        user.birth_date = birth_date
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
    if request.user == reservation.user:
        reservation.delete()
    return redirect('reserved_travels')

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

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})

@login_required
def list_travels(request):
    travels = Travel.objects.all()
    username = request.user.username
    context = {
        'username': username,
        'travel_list': travels,
    }
    return render(request, 'myfirstapp/List_travels.html', context)

def delete_travel(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    travel.delete()
    return JsonResponse({'message': 'Travel deleted successfully'})

def add_promotion(request):
    context = {}
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save()
            selected_travel = form.cleaned_data['travel']
            selected_travel.promotion = promotion
            selected_travel.save()
            return redirect('add_promotion')
    else:
        form = PromotionForm()
    context['username'] = request.user.username
    return render(request, 'myfirstapp/promotions.html',  {'form': form, **context})
