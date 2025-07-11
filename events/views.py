from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.order_by('date')[:3]  # limit to 3 upcoming
    return render(request, 'events/event_list.html', {'events': events})
