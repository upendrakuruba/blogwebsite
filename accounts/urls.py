from django.urls import path
from .views import *
urlpatterns = [
    path('login/', login, name='login'),
    path('Logout_view/', Logout_view, name='Logout_view'),
    path('registration/', customerregistration, name='registration'),
    path("activate/<uidb64>/<token>/",activate, name="activate"),
    path("forgotpassword/", forgotpassword, name="forgotpassword"),
    path("resetpassword_validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword_validate"),
    path("resetpassword/", resetpassword, name="resetpassword"),
    path('changepassword/', change_password, name='changepassword'),
]
