from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import render
import re

def home(request):
    return render(request, 'index.html')

def check_restrictions(request):
    plate = request.GET.get('plate', '').strip().upper()
    date_input = request.GET.get('date', '')

    if not plate or not date_input:
        return JsonResponse({'error': 'Please enter both license plate and date'}, status=400)

    # Validate plate format
    plate_regex = r'^[A-Z]{2,3}-?\d{3,4}$'
    if not re.match(plate_regex, plate):
        return JsonResponse({'error': 'Invalid license plate format. Use format like PBX-1234'}, status=400)

    last_digit = [char for char in plate if char.isdigit()][-1]
    date = datetime.strptime(date_input, "%Y-%m-%d")
    day_of_week = date.weekday()

    # Define restriction rules
    restriction_map = {
        0: ['1', '2'],  # Monday
        1: ['3', '4'],  # Tuesday
        2: ['5', '6'],  # Wednesday
        3: ['7', '8'],  # Thursday
        4: ['9', '0'],  # Friday
    }

    can_circulate = last_digit not in restriction_map.get(day_of_week, [])
    day_name = date.strftime('%A')
    formatted_date = date.strftime('%A, %B %d, %Y')

    if can_circulate:
        result = {
            'message': f'Your vehicle CAN circulate on {formatted_date}',
            'plate': plate,
            'date': formatted_date,
            'day': day_name,
            'can_circulate': True
        }
    else:
        result = {
            'message': f'Your vehicle CANNOT circulate on {formatted_date}',
            'plate': plate,
            'date': formatted_date,
            'day': day_name,
            'can_circulate': False
        }

    return JsonResponse(result)