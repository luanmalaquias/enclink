from os import name
from django.urls import path
from .views import *
from django.conf import urls

urlpatterns = [
    path("", home, name="home"),
    path("r/<str:link>/", redirecionar),
    path("login/", encLinkUser, name="enclink-user"),
    path("logout/", logoutUser, name="logout"),
    path("logs/", logs, name="logs"),
    path("logs/delete/<str:id>", deletar, name="deletar")
]

urls.handler404 = handlerErrorPage