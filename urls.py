from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register_user),
    path('users/login', views.login),
    path('user/<int:quote_user_id>', views.profile),
    path('delete/<int:quote_id>', views.delete_quote),
    path('myaccount/<int:user_id>', views.edit_page),
    path('update/<int:user_id>', views.update_user),
    path('logout', views.logout),
]
