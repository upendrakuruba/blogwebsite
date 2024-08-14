from django.urls import path
from .views import *
urlpatterns = [
    path("Aboutpage/", Aboutpage, name="About"),
    path("Contactpage/", Contactpage, name="Contact")
]

