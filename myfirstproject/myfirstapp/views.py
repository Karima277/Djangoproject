from django.shortcuts import render
from .models import Travel
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

def home(request):
    return render(request, 'myfirstapp/index.html')
def profile(request):
    return render(request,'myfirstapp/profile.html')
def signup(request):
    return render(request, 'myfirstapp/signup.html')

# def login(request):
#     return render(request, 'myfirstapp/login.html')
def travels(request):
    context={'Travels': Travel.objects.all()}
    return render(request, 'myfirstapp/travels.html',context)
# views.py



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