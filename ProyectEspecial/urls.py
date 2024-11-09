from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(),
         name='login'),  # Ruta para el login
    # URLs de autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    # URLs de la aplicación
    path('reveloper/', include('Reveloper.urls')),
]
