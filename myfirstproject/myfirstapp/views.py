from django.shortcuts import render
from .models import Travel,CustomUser
from django.db.models import Q
from .models import Promotion
from django.shortcuts import redirect
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
# views.py
from .forms import LoginForm  # Import your LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render, get_object_or_404
from .models import Travel
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from .forms import PromotionForm

def home(request):
    return render(request, 'myfirstapp/index.html')
def profile(request):
    return render(request,'myfirstapp/profile.html')
def signup(request):
    return render(request, 'myfirstapp/signup.html')
def cart(request):
    return render(request, 'myfirstapp/cart.html')
def success(request):
    return render(request, 'myfirstapp/success.html')

def travel_details(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    return render(request, 'myfirstapp/details.html', {'travel': travel})
# def login(request):
#     return render(request, 'myfirstapp/login.html')
def travels(request):
    context={'Travels': Travel.objects.all()}
    return render(request, 'myfirstapp/travels.html',context)
# views.py
def Reservation(request):
    return render(request, 'myfirstapp/Reservation.html')


def search_results(request):
    if request.method == 'GET':
        # Get the form data
        max_price = request.GET.get('max_price')
        destination = request.GET.get('destination')
        duration = request.GET.get('duration')

        # Print form data
        print(f"max_price: {max_price}, destination: {destination}, duration: {duration}")

        # Filter travels based on form data
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
                # Handle the case where the conversion to int fails
                pass

        # Print the number of travels after filtering
        print(f"Number of travels after filtering: {travels.count()}")
        #travels = [apply_promotion(travel) for travel in travels]
        # Pass the filtered travels to the template
        return render(request, 'myfirstapp/search_results.html', {'travels': travels})
from datetime import date

def apply_promotion(travel):
    promotion = travel.promotion
    if promotion and promotion.start_date <= date.today() <= promotion.end_date:
        travel.price -= travel.price * (promotion.discount_percentage / 100)
    return travel
# views.py


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Additional logic like login the user, send confirmation email, etc.
            return redirect('home_page')  # Redirect to the home page or any other desired page
    else:
        form = SignUpForm()

    return render(request, 'myfirstapp/signup.html', {'form': form})





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Login the user
            user = form.get_user()
            login(request, user)
            return redirect('home_page')  # Redirect to a success page
    else:
        form = LoginForm()

    return render(request, 'myfirstapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')


from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Reservation, Travel

@login_required
def reserve(request, travel_id):
    # Retrieve the Travel object
    travel = get_object_or_404(Travel, id=travel_id)

    if request.method == 'POST':
        # Retrieve form data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        card_number = request.POST.get('cardnumber')
        expiration_date = request.POST.get('expiration')
        cvv = request.POST.get('cvv')

        # Create a reservation object and save it to the database
        reservation = Reservation(
            user=request.user,
            travel=travel,  # Associate the Travel with the Reservation
            name=name,
            email=email,
            address=address,
            card_number=card_number,
            expiration_date=expiration_date,
            cvv=cvv
        )
        reservation.save()

        # You can add additional logic or redirect the user to a success page
        return redirect('success_page')

    return render(request, 'your_template.html', {'travel': travel})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

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
    # Get travels that the user has reserved
    reserved_travels = Travel.objects.filter(reservation__user=request.user)

    context = {
        'reserved_travels': reserved_travels,
    }

    return render(request, 'myfirstapp/Reservation.html', context)

from django.shortcuts import get_object_or_404, redirect
from .models import Reservation

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Check if the user making the request is the owner of the reservation
    if request.user == reservation.user:
        reservation.delete()
        # You can add a success message or perform other actions here
    else:
        # Redirect or handle unauthorized cancellation attempts
        pass

    # Redirect to a success page or any other desired page
    return redirect('reserved_travels')
from django.contrib.auth import get_user_model
def administrator_dashboard(request):
    username = request.user.username
    #last_five_users = CustomUser.objects.all().order_by('-id')[:5]
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
        'user_list':users,
     }
    return render(request, 'myfirstapp/Clients.html', context )
from django.http import JsonResponse
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Travel

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
            # Save the promotion first
            promotion = form.save()

            # Get the selected travel
            selected_travel = form.cleaned_data['travel']

            # Associate the promotion with the selected travel
            selected_travel.promotion = promotion
            selected_travel.save()

            return redirect('add_promotion')  # Redirect to a view displaying the list of promotions

    else:
        form = PromotionForm()
    context['username'] = request.user.username
    return render(request, 'myfirstapp/promotions.html',  {'form': form, **context})
