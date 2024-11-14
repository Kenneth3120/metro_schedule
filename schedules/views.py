from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import pandas as pd
import pytz

from .forms import ProfileForm, FeedbackForm
from .models import Profile, Feedback

# Set timezone to IST once at the start
ist = pytz.timezone('Asia/Kolkata')

def home(request):
    current_time = datetime.now(ist).time()
    stations = []
    next_metro = None
    selected_station = None
    trip_type = 'onward'
    minutes_until_next_metro = None

    # Load stations list from the default schedule
    onward_schedule_path = 'pune_metro_full_day_schedule.csv'
    try:
        onward_schedule_df = pd.read_csv(onward_schedule_path)
        stations = onward_schedule_df['Station Name'].unique()
    except FileNotFoundError:
        messages.error(request, f"File '{onward_schedule_path}' not found.")
        return render(request, 'home.html', {'stations': stations})

    # Generate greeting message for authenticated users
    if request.user.is_authenticated:
        hour = current_time.hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        messages.info(request, f"Hello {request.user.username}, {greeting}!")

    # Handle station selection and trip type
    if request.method == 'POST':
        selected_station = request.POST.get('station')
        trip_type = request.POST.get('trip_type', 'onward')
        schedule_path = (
            'pune_metro_full_day_schedule.csv' if trip_type == 'onward' 
            else 'pune_metro_full_day_schedule_return.csv'
        )

        try:
            schedule_df = pd.read_csv(schedule_path)
        except FileNotFoundError:
            messages.error(request, f"File '{schedule_path}' not found.")
            return render(request, 'home.html', {'stations': stations, 'selected_station': selected_station})

        # Filter schedule for selected station and find next metro timing
        station_schedule = schedule_df[schedule_df['Station Name'] == selected_station]
        try:
            upcoming_times = station_schedule['Scheduled Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
            next_metro_time = min((time for time in upcoming_times if time > current_time), default=None)

            if next_metro_time:
                next_metro = next_metro_time
                time_difference = datetime.combine(datetime.today(), next_metro_time) - datetime.combine(datetime.today(), current_time)
                minutes_until_next_metro = time_difference.total_seconds() // 60
        except Exception as e:
            messages.error(request, f"Error parsing schedule times: {e}")

    return render(request, 'home.html', {
        'stations': stations,
        'selected_station': selected_station,
        'next_metro': next_metro,
        'trip_type': trip_type,
        'minutes_until_next_metro': minutes_until_next_metro,
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
    # Clear any previous messages to avoid displaying "logged out successfully" on login
    storage = messages.get_messages(request)
    storage.used = True

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

def user_logout(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True  # Clear the message queue to prevent showing on next login
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error saving profile. Please check your input.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.user = request.user
            feedback_instance.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedbacks})

@login_required
def edit_feedback(request, feedback_id):
    feedback_instance = get_object_or_404(Feedback, id=feedback_id, user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully!")
            return redirect('feedback')
    else:
        form = FeedbackForm(instance=feedback_instance)

    return render(request, 'edit_feedback.html', {'form': form})

@login_required
def delete_feedback(request, feedback_id):
    feedback_instance = get_object_or_404(Feedback, id=feedback_id, user=request.user)
    feedback_instance.delete()
    messages.success(request, "Feedback deleted successfully!")
    return redirect('feedback')
