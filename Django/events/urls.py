from django.urls import path
from .views import index, get, add, edit, delete

app_name = 'events'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('<int:id>/', get, name='get'),
    path('<int:id>/edit/', edit, name='edit'),
    path('<int:id>/delete/', delete, name='delete'),
]
