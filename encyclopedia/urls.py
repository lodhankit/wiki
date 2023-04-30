from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.details, name="title"),
    path("add/", views.create, name='add'),
    path("random/", views.enter, name="random")
]
