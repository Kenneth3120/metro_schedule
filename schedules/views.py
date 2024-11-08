from django.shortcuts import render
import pandas as pd
from datetime import datetime

def home(request):
    # Load metro schedule from CSV
    schedule_df = pd.read_csv('pune_metro_adjusted_day_schedule.csv')
    
    # Get the list of station names from the CSV
    stations = schedule_df['Station Name'].unique()

    next_metro = None
    selected_station = None

    # Handle form submission
    if request.method == 'POST':
        selected_station = request.POST.get('station')
        current_time = datetime.now().time()

        # Filter schedule for the selected station and find next metro timing
        station_schedule = schedule_df[schedule_df['Station Name'] == selected_station]
        upcoming_times = station_schedule['Scheduled Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
        next_metro = min((time for time in upcoming_times if time > current_time), default=None)

    return render(request, 'home.html', {
        'stations': stations,
        'selected_station': selected_station,
        'next_metro': next_metro,
    })
