from django.shortcuts import render, redirect
import pandas as pd
from datetime import datetime
import pytz
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os


def home(request):
    # Set timezone to IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).time()

    # Initialize variables
    stations = []
    next_metro = None
    selected_station = None
    trip_type = 'onward'

    # Load stations list from onward trip CSV by default
    onward_schedule_path = 'pune_metro_full_day_schedule.csv'
    try:
        onward_schedule_df = pd.read_csv(onward_schedule_path)
        stations = onward_schedule_df['Station Name'].unique()
    except FileNotFoundError:
        messages.error(request, f"File '{onward_schedule_path}' not found.")
        return render(request, 'home.html', {
            'stations': stations,
            'selected_station': selected_station,
            'next_metro': next_metro,
            'trip_type': trip_type,
        })

    # Handle form submission
    if request.method == 'POST':
        selected_station = request.POST.get('station')
        trip_type = request.POST.get('trip_type', 'onward')

        # Choose the appropriate CSV based on trip type
        schedule_path = 'pune_metro_full_day_schedule.csv' if trip_type == 'onward' else 'pune_metro_full_day_schedule_return.csv'
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
            next_metro = min((time for time in upcoming_times if time > current_time), default=None)
        except Exception as e:
            messages.error(request, f"Error parsing schedule times: {e}")
    
    return render(request, 'home.html', {
        'stations': stations,
        'selected_station': selected_station,
        'next_metro': next_metro,
        'trip_type': trip_type,
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
