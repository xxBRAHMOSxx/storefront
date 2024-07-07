from django.urls import path
from . import views

# sub URLConfig needs to be imported in the main url file
urlpatterns = [
    # views.say_hello is a reference no calling a function
    path('hello/', views.say_hello)
]
