from django.urls import path
from .views import login_usuario, logout_usuario, registrar_usuario

urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('registro/', registrar_usuario, name='registrar'),
]
