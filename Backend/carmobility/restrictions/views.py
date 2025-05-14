from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import render
import re

def home(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        plate = request.POST.get('plate')
        date = request.POST.get('date')
        time = request.POST.get('time')

        plate_regex = r'^[A-Z]{2,3}-?\d{3,4}$'
        if not re.match(plate_regex, plate):
            return render(request, 'index.html', {'error': 'Invalid license plate format. Use format like PBX-1234'})

        plate = plate.strip().upper() if plate else ''

        if not plate or not date or not time:
            return render(request, 'index.html', {'error': 'Please enter license plate, date, and time'})
        
        last_digit = [char for char in plate if char.isdigit()][-1]
        date = datetime.strptime(date, "%Y-%m-%d")
        time = datetime.strptime(time, "%H:%M")
        day_of_week = date.weekday()

        # Convert time to minutes since midnight for easier comparison
        total_minutes = time.hour * 60 + time.minute

        # Define restriction hours for morning and afternoon
        morning_start = 6 * 60   # 6:00 AM
        morning_end = 9 * 60 + 30 # 9:30 AM
        afternoon_start = 16 * 60  # 4:00 PM
        afternoon_end = 20 * 60    # 8:00 PM

        # Check if the time is within restricted periods
        is_restricted_time = (morning_start <= total_minutes <= morning_end) or (afternoon_start <= total_minutes <= afternoon_end)

        # Define restriction rules based on the last digit of the plate number
        restriction_map = {
            0: ['1', '2'],  # Monday
            1: ['3', '4'],  # Tuesday
            2: ['5', '6'],  # Wednesday
            3: ['7', '8'],  # Thursday
            4: ['9', '0'],  # Friday
        }

        # Check if it's a restricted day based on plate last digit
        is_restricted_day = last_digit in restriction_map.get(day_of_week, [])

        # Determine if the vehicle can circulate
        can_circulate = not (is_restricted_day and is_restricted_time)

        # Format date for display
        formatted_date = date.strftime('%A, %B %d, %Y')
        formatted_time = time.strftime('%I:%M %p')

        # Return result as JSON
        if can_circulate:
            result = {
                'message': f'Your vehicle CAN circulate on {formatted_date} at {formatted_time}',
                'plate': plate,
                'date': formatted_date,
                'time': formatted_time,
                'can_circulate': True
            }
        else:
            restriction_period = "morning (6:00 AM - 9:30 AM)" if morning_start <= total_minutes <= morning_end else "afternoon (4:00 PM - 8:00 PM)"
            result = {
                'message': f'Your vehicle CANNOT circulate on {formatted_date} at {formatted_time}',
                'plate': plate,
                'date': formatted_date,
                'time': formatted_time,
                'can_circulate': False,
                'restriction_period': restriction_period
            }

        return render(request, 'index.html', {'result': result})