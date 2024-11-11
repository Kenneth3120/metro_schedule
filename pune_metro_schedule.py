import csv
from datetime import datetime, timedelta

# Define station names and initial scheduled times for the first round (Vanaz to Ramwadi)
stations = [
    ("Vanaz", "06:00:00"),
    ("Anand Nagar", "06:02:28"),
    ("Ideal Colony", "06:04:56"),
    ("Nal Stop", "06:07:24"),
    ("Garware College", "06:09:52"),
    ("Deccan Gymkhana", "06:12:20"),
    ("Chatrapati Sambhaji Udyan", "06:14:48"),
    ("PMC", "06:17:16"),
    ("District Court", "06:19:44"),
    ("Mangalwar Peth", "06:22:12"),
    ("Pune Railway Station", "06:24:40"),
    ("Ruby Hall Clinic", "06:27:08"),
    ("Bund Garden", "06:29:36"),
    ("Yerwada", "06:32:04"),
    ("Kalyani Nagar", "06:34:32"),
    ("Ramwadi", "06:37:00")
]

# Define time intervals for peak and non-peak hours
non_peak_interval = timedelta(minutes=10)
peak_interval = timedelta(minutes=7)

# Define peak and non-peak hour ranges
non_peak_hours = [
    (datetime.strptime("06:00", "%H:%M"), datetime.strptime("08:00", "%H:%M")),
    (datetime.strptime("11:00", "%H:%M"), datetime.strptime("16:00", "%H:%M")),
    (datetime.strptime("20:00", "%H:%M"), datetime.strptime("22:00", "%H:%M"))
]
peak_hours = [
    (datetime.strptime("08:00", "%H:%M"), datetime.strptime("11:00", "%H:%M")),
    (datetime.strptime("16:00", "%H:%M"), datetime.strptime("20:00", "%H:%M"))
]

# Function to check if a time is in peak hours
def is_peak_hour(time):
    for start, end in peak_hours:
        if start.time() <= time.time() < end.time():
            return True
    return False

# Start creating the schedule from 6:00 AM to 10:00 PM
start_time = datetime.strptime("06:00", "%H:%M")
end_time = datetime.strptime("22:00", "%H:%M")

# Prepare rows to write into the CSV file
schedule_rows = []
current_time = start_time

while current_time < end_time:
    # Determine the interval based on peak/non-peak time
    interval = peak_interval if is_peak_hour(current_time) else non_peak_interval

    # Calculate scheduled times for each station based on the current start time
    schedule_for_trip = []
    trip_start_time = current_time
    for station, base_time in stations:
        # Calculate the scheduled time for the station relative to trip start time
        base_minutes = datetime.strptime(base_time, "%H:%M:%S") - datetime.strptime("06:00:00", "%H:%M:%S")
        station_time = trip_start_time + base_minutes
        schedule_for_trip.append((trip_start_time.strftime("%H:%M:%S"), station, station_time.strftime("%H:%M:%S")))

    # Add the trip schedule to the rows
    schedule_rows.extend(schedule_for_trip)
    schedule_rows.append(("", "", ""))  # Blank line to separate trips

    # Move to the next trip time
    current_time += interval

# Save the schedule to a CSV file
output_file_path = "pune_metro_full_day_schedule.csv"
with open(output_file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Train Start Time", "Station Name", "Scheduled Time"])
    writer.writerows(schedule_rows)

print(f"Schedule saved to {output_file_path}")
