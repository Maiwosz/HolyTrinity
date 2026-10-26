from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import News
from .forms import NewsForm

# Create your views here.


def index(request):
    # Pobranie pozycji z bazy danych
    news = News.objects.order_by('-create_time')
    # Stworzenie słownika przechowującego elementy
    # bazy danych pod zmienną news
    context = {'news': news}
    # Przesłanie wyrenderowanej strony wraz z dodanymi
    # elementami z bazy danych
    return render(request, 'news/index.html', context)


@login_required(login_url='/login/')
def add(request):
    # Jeżeli POST - szukamy danych w ciele zapytania
    # Jeżeli GET - wysyłamy formularz do wypełnienia
    if request.method == 'POST':
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        news = NewsForm(request.POST)
        if news.is_valid():
            news = news.save(commit=False)
            # news.author = request.user
            news.create_time = timezone.now()
            news.last_edit_time = timezone.now()
            news.save()
            return redirect('view_news')
        # Jeżeli dane nie są prawidłowe - odsyłamy formularz z błędami
        else:
            context = {'form': news}
            return render(request, 'news/add.html', context)
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        news = NewsForm()
        context = {'form': news}
        return render(request, 'news/add.html', context)


def get(request, id):
    # get_object_or_404 zwraca element z bazy danych
    # lub przesyła do klienta błąd 404
    news = get_object_or_404(News, id=id)
    context = {'news': news}
    return render(request, 'news/view.html', context)


@login_required(login_url='/login/')
def edit(request, id):
    # Pobranie edytowanego elementu z bazy danych lub błąd 404
    news = get_object_or_404(News, id=id)
    # Jeżeli POST - aktualizujemy istniejący element danymi z formularza
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.last_edit_time = timezone.now()
            news.save()
            return redirect('get', id=news.id)
        # Jeżeli dane nie są prawidłowe - odsyłamy formularz z błędami
        else:
            context = {'form': form, 'news': news}
            return render(request, 'news/edit.html', context)
    # Jeżeli GET - przesyłamy formularz wypełniony aktualnymi danymi
    else:
        form = NewsForm(instance=news)
        context = {'form': form, 'news': news}
        return render(request, 'news/edit.html', context)
