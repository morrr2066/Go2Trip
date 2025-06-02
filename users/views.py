from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from trips.models import Trip
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()  # This triggers the signal to create Profile

            # Now update the profile birthday
            birthday = form.cleaned_data['birthday']
            user.profile.birthday = birthday
            user.profile.save()

            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # change 'home' to your homepage URL name
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    user_trips = Trip.objects.filter(creator=request.user)
    return render(request, 'users/profile.html', {
        'user': request.user,
        'trips': user_trips
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture')

        profile = request.user.profile
        profile.bio = bio

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        return redirect('profile')  # assuming 'profile' is your profile page URL name

    return redirect('profile')
