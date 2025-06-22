from django.contrib import admin
from django.urls import path, include
from mailings.views import HomeView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('clients/', include('clients.urls')),
    path('messages/', include('mail_messages.urls')),
    path('mailings/', include('mailings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/', include('allauth.urls')),
]
