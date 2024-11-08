from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(),
         name='login'),  # Ruta para el login
    # Incluye las URLs de autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    # Incluye las URLs de tu aplicación
    path('reveloper/', include('Reveloper.urls')),
]
