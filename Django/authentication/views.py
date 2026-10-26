from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.


def log_in(request):
    # Jeżeli użytkownik jest zalogowany - przekierowanie na listę wiadomości
    if request.user.is_authenticated:
        return redirect('view_news')

    # Jeżeli POST - próba zalogowania użytkownika
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Sprawdzenie czy użytkownik istnieje w bazie danych
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            # Jeżeli istnieje - zalogowanie i przekierowanie
            if user is not None:
                login(request, user)
                return redirect('view_news')
            # Jeżeli nie istnieje - odesłanie formularza z danymi
            else:
                context = {'form': form}
                return render(request, 'authentication/login.html', context)
        else:
            context = {'form': form}
            return render(request, 'authentication/login.html', context)
    # Jeżeli GET - przesłanie pustego formularza
    else:
        context = {'form': LoginForm()}
        return render(request, 'authentication/login.html', context)


def log_out(request):
    # Wylogowanie użytkownika (usunięcie sesji) i przekierowanie
    # na stronę główną
    logout(request)
    return redirect('index')
