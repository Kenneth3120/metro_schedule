from django.shortcuts import render, redirect
import pandas as pd
from datetime import datetime
import pytz
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import logout

# Set timezone to IST once at the start
ist = pytz.timezone('Asia/Kolkata')

def home(request):
    # Initialize variables
    current_time = datetime.now(ist).time()
    stations = []
    next_metro = None
    selected_station = None
    trip_type = 'onward'
    minutes_until_next_metro = None  # Initialize the minutes variable

    # Load stations list from onward trip CSV by default
    onward_schedule_path = 'pune_metro_full_day_schedule.csv'
    try:
        onward_schedule_df = pd.read_csv(onward_schedule_path)
        stations = onward_schedule_df['Station Name'].unique()
    except FileNotFoundError:
        messages.error(request, f"File '{onward_schedule_path}' not found.")
        return render(request, 'home.html', {'stations': stations})

    # Generate greeting message if the user is authenticated
    if request.user.is_authenticated:
        hour = current_time.hour
        if hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        messages.info(request, f"Hello {request.user.username}, {greeting}!")

    # Handle form submission
    if request.method == 'POST':
        selected_station = request.POST.get('station')
        trip_type = request.POST.get('trip_type', 'onward')

        # Choose the appropriate CSV based on trip type
        schedule_path = (
            'pune_metro_full_day_schedule.csv' if trip_type == 'onward' 
            else 'pune_metro_full_day_schedule_return.csv'
        )
        try:
            schedule_df = pd.read_csv(schedule_path)
        except FileNotFoundError:
            messages.error(request, f"File '{schedule_path}' not found.")
            return render(request, 'home.html', {
                'stations': stations,
                'selected_station': selected_station,
                'next_metro': next_metro,
                'trip_type': trip_type,
            })

        # Filter schedule for the selected station and find next metro timing
        station_schedule = schedule_df[schedule_df['Station Name'] == selected_station]
        try:
            upcoming_times = station_schedule['Scheduled Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())

            # Find the next metro time that is after the current time
            next_metro_time = min((time for time in upcoming_times if time > current_time), default=None)

            if next_metro_time:
                next_metro = next_metro_time
                # Calculate the difference in minutes
                next_metro_datetime = datetime.combine(datetime.today(), next_metro_time)
                current_datetime = datetime.combine(datetime.today(), current_time)
                time_difference = next_metro_datetime - current_datetime
                minutes_until_next_metro = time_difference.total_seconds() // 60  # Get the difference in minutes
        except Exception as e:
            messages.error(request, f"Error parsing schedule times: {e}")

    return render(request, 'home.html', {
        'stations': stations,
        'selected_station': selected_station,
        'next_metro': next_metro,
        'trip_type': trip_type,
        'minutes_until_next_metro': minutes_until_next_metro,  # Pass the minutes to the template
    })
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")  # Display a success message
            return redirect('profile')  # Redirect to refresh the profile page and show updated data
        else:
            messages.error(request, "Error saving profile. Please check your input.")  # Show error message if form is invalid
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

def user_logout(request):
    logout(request)  # Log the user out
    messages.success(request, "Logged out successfully!")  # Optional: success message for logout
    return redirect('login')  # Redirect to the login page after logging out