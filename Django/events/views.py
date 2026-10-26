from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm

# Create your views here.
# Wszystkie widoki aplikacji są dostępne tylko po zalogowaniu


@login_required(login_url='/login/')
def index(request):
    # Lista wydarzeń posortowana po dacie
    events = Event.objects.order_by('date')
    context = {'events': events}
    return render(request, 'events/index.html', context)


@login_required(login_url='/login/')
def get(request, id):
    event = get_object_or_404(Event, id=id)
    context = {'event': event}
    return render(request, 'events/view.html', context)


@login_required(login_url='/login/')
def add(request):
    # Jeżeli POST - zapis nowego elementu, jeżeli GET - pusty formularz
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('events:get', id=event.id)
    else:
        form = EventForm()
    # Pusty formularz lub formularz z błędami
    context = {'form': form}
    return render(request, 'events/form.html', context)


@login_required(login_url='/login/')
def edit(request, id):
    event = get_object_or_404(Event, id=id)
    # Formularz powiązany z istniejącym elementem (instance)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:get', id=event.id)
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'event': event}
    return render(request, 'events/form.html', context)


@login_required(login_url='/login/')
def delete(request, id):
    event = get_object_or_404(Event, id=id)
    # Usunięcie tylko przez POST - GET wyświetla stronę potwierdzenia
    if request.method == 'POST':
        event.delete()
        return redirect('events:index')
    context = {'event': event}
    return render(request, 'events/delete.html', context)
