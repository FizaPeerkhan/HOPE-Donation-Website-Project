from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Donor_Registers, Ngo_Registers, CustomUser
from .forms import DonorRegistrationForm, NgoRegistrationForm, DonorLoginForm, NGOLoginForm

# Donor Registration
def register(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type='donor',
                is_donor=True
            )
            donor = form.save(commit=False)
            donor.user = user
            donor.save()

            messages.success(request, "Registration successful! Please log in.")
            return redirect('login-page')
    else:
        form = DonorRegistrationForm()

    return render(request, 'registration/donor-register.html', {'form': form})

# NGO Registration
def ngo_register(request):
    if request.method == 'POST':
        form = NgoRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type='ngo',
                is_ngo=True
            )
            ngo = form.save(commit=False)
            ngo.user = user
            ngo.save()

            messages.success(request, "NGO registration successful! Please log in.")
            return redirect('login-page')
    else:
        form = NgoRegistrationForm()

    return render(request, 'registration/register-ngo.html', {'form': form})

# Login for both Donor and NGO
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('login-page')
        if user is not None:
            login(request, user)  # Logs the user in
            messages.success(request, "Login successful!")

        # Redirect based on user type
        if user_type == 'donor':
            if user.is_donor:
                return redirect('index')
            else:
                messages.error(request, "User is not a donor")
                return redirect('login-page')
        elif user_type == 'ngo':
            if user.is_ngo:
                return redirect('ngo_dashboard')
            else:
                messages.error(request, "User is not an NGO")
                return redirect('login-page')
        else:
            return redirect('index')  # Default redirect

    return render(request, 'registration/login.html')

# Homepages
def index(request):
    return render(request, 'registration/index.html')

def ngo_dashboard(request):
    return render(request, 'registration/ngo-dashboard.html')