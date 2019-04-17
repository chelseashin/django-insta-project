from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),
    path('edit/', views.update, name='update'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    ]