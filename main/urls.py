from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import path
from .views import home, about, register, login_view, profile, transfer, transfer_confirm, transaction_history, history, logout_view

app_name = "main"

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('sign-up/', register, name="register"),
    path('login/', login_view, name="login"),
    path('dashboard/<int:pk>/home', profile, name="profile"),
    path('transfer/', transfer, name="transfer"),
    path('transfer/confirmation/<ref>', transfer_confirm, name="confirmation"),
    path('<us>/transaction_history', transaction_history, name="history"),
    path('transaction/<ref>', history, name="details"),
    path('logout/', logout_view, name="logout")
]